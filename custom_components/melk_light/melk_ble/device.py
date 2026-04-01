"""BLE connection + device state for MELK LED bar."""

from __future__ import annotations

import asyncio
import logging
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass

from bleak import BleakClient
from bleak.backends.device import BLEDevice
from bleak_retry_connector import establish_connection

from .constants import CHARACTERISTIC_UUID, DEVICE_NAME_PREFIX
from .protocol import (
    packet_brightness,
    packet_color,
    packet_color_temperature,
    packet_rgbw_status,
    packet_single_color,
    packet_mic_eq_mode,
    packet_mic_onoff,
    packet_mic_sensitivity,
    packet_mode,
    packet_mode_speed,
    packet_power,
    packet_scene,
)

_LOGGER = logging.getLogger(__name__)

# The FFF3 characteristic is Write-Without-Response only (no ACK).
# We improve reliability by sending each packet _WRITE_REPEAT_COUNT times,
# matching the reference app's 100 ms periodic-timer approach.
_WRITE_REPEAT_COUNT = 2    # how many times to send each packet (app: 1x, +1 for ESPHome proxy)
_WRITE_REPEAT_DELAY = 0.1  # seconds between repeats (≈ app's 100 ms interval)
_POST_CONNECT_DELAY = 0.3  # settle time after a fresh BLE connection
_DISCONNECT_TIMEOUT = 30.0 # seconds of inactivity before dropping the connection


@dataclass
class MelkState:
    is_on: bool = False
    brightness: int | None = None
    rgb: tuple[int, int, int] | None = None
    single_color: int | None = None
    warm: int | None = None
    cold: int | None = None
    mode: int | None = None
    mode_speed: int | None = None
    scene: int | None = None
    mic_on: bool | None = None
    mic_sensitivity: int | None = None
    mic_eq_mode: int | None = None


class MelkLedDevice:
    """Connection + write throttling for MELK LED bar.

    Each public method sends exactly one packet, matching the reference app
    (melk_led_controller.py / BluetoothLEService.java).
    """

    def __init__(self, address: str) -> None:
        self.address = address
        self.client: BleakClient | None = None
        self.name: str | None = None
        self._ble_device: BLEDevice | None = None  # stored for reconnect
        self._lock = asyncio.Lock()
        self._last_tx = 0.0
        self.state = MelkState()
        self._disconnect_timer: asyncio.TimerHandle | None = None

    def _on_disconnect(self, client: BleakClient) -> None:  # noqa: ARG002
        _LOGGER.debug("Disconnected from MELK device %s", self.address)
        self.client = None
        if self._disconnect_timer:
            self._disconnect_timer.cancel()
            self._disconnect_timer = None

    def _reset_disconnect_timer(self) -> None:
        if self._disconnect_timer:
            self._disconnect_timer.cancel()
            
        loop = asyncio.get_running_loop()
        self._disconnect_timer = loop.call_later(
            _DISCONNECT_TIMEOUT,
            lambda: asyncio.create_task(self._auto_disconnect())
        )

    async def _auto_disconnect(self) -> None:
        _LOGGER.debug("No commands sent for %s seconds, automatically disconnecting %s", _DISCONNECT_TIMEOUT, self.address)
        await self.disconnect()

    def is_connected(self) -> bool:
        return bool(self.client and self.client.is_connected)

    async def connect(self, ble_device: BLEDevice) -> bool:
        self._ble_device = ble_device  # always refresh so reconnect is possible
        if self.is_connected():
            return True
        try:
            _LOGGER.debug("Connecting to MELK device %s", self.address)
            self.client = await establish_connection(
                BleakClient,
                ble_device,
                ble_device.address,
                disconnected_callback=self._on_disconnect,
            )
            if not self.client.is_connected:
                return False
            if not self.name:
                self.name = ble_device.name or DEVICE_NAME_PREFIX.rstrip("-")
            _LOGGER.debug("Connected to MELK device %s", self.address)
            return True
        except Exception as err:
            _LOGGER.warning("Failed to connect to %s: %s", ble_device.address, err)
            self.client = None
            return False

    async def disconnect(self) -> None:
        if self._disconnect_timer:
            self._disconnect_timer.cancel()
            self._disconnect_timer = None

        if not self.client:
            return
        try:
            if self.client.is_connected:
                _LOGGER.debug("Disconnecting from MELK device %s...", self.address)
                await self.client.disconnect()
        except Exception as err:
            _LOGGER.debug("Disconnect error: %s", err)
        finally:
            self.client = None

    async def _write(self, data: bytes) -> None:
        """Write Without Response, sent _WRITE_REPEAT_COUNT times for reliability.

        The FFF3 characteristic only supports Write Without Response
        (GATT error 3 / ATT_ERR_WRITE_NOT_PERMITTED with response=True).
        There is no ACK, so we compensate by sending each packet multiple
        times with a ~100 ms gap — matching the reference app's timer approach.
        On connection loss the client is reconnected before the next send.
        """
        async with self._lock:
            now = time.monotonic()
            gap = now - self._last_tx
            if gap < _WRITE_REPEAT_DELAY:
                await asyncio.sleep(_WRITE_REPEAT_DELAY - gap)

            for n in range(1, _WRITE_REPEAT_COUNT + 1):
                # Reconnect if the connection was lost between sends.
                if not self.client or not self.client.is_connected:
                    if self._ble_device is None:
                        raise RuntimeError("No BLE device available for reconnect")
                    _LOGGER.debug(
                        "Reconnecting before send %d/%d …", n, _WRITE_REPEAT_COUNT
                    )
                    if not await self.connect(self._ble_device):
                        raise RuntimeError(
                            f"Reconnect failed before send {n}/{_WRITE_REPEAT_COUNT}"
                        )
                    await asyncio.sleep(_POST_CONNECT_DELAY)

                self._last_tx = time.monotonic()
                _LOGGER.debug("TX [%d/%d] %s", n, _WRITE_REPEAT_COUNT, data.hex())
                await self.client.write_gatt_char(
                    CHARACTERISTIC_UUID, data, response=False
                )

                if n < _WRITE_REPEAT_COUNT:
                    await asyncio.sleep(_WRITE_REPEAT_DELAY)

    async def ensure_connected(self, ble_device: BLEDevice) -> None:
        was_connected = self.is_connected()
        if not await self.connect(ble_device):
            raise RuntimeError(f"Unable to connect to {ble_device.address}")
        if not was_connected:
            await asyncio.sleep(_POST_CONNECT_DELAY)

    @asynccontextmanager
    async def connected(self, ble_device: BLEDevice):
        """Ensure the device is connected for a command block.

        The connection is kept alive after the block exits so that subsequent
        commands can reuse it without paying the reconnect cost each time.
        It will automatically disconnect after 30 seconds of inactivity.
        Call disconnect() explicitly (e.g. on integration unload) when the
        connection is no longer needed.
        """
        if self._disconnect_timer:
            self._disconnect_timer.cancel()
            self._disconnect_timer = None

        await self.ensure_connected(ble_device)
        try:
            yield
        finally:
            self._reset_disconnect_timer()

    # ── Commands (each sends exactly one packet) ──────────────

    async def power(self, on: bool) -> None:
        await self._write(packet_power(on))
        self.state.is_on = on

    async def set_brightness(self, brightness: int, light_mode: int = 0xFF) -> None:
        b = max(0, min(255, int(brightness)))
        await self._write(packet_brightness(b, light_mode))
        self.state.brightness = b

    async def set_rgb(self, r: int, g: int, b: int) -> None:
        await self._write(packet_color(r, g, b))
        self.state.rgb = (r & 0xFF, g & 0xFF, b & 0xFF)

    async def set_color_temperature(self, warm: int, cold: int) -> None:
        # The reference app's UI works in a 0..100 scale for CT sliders.
        # Sending 0..255 here can cause some devices to interpret values as OFF/reset.
        w = max(0, min(100, int(warm)))
        c = max(0, min(100, int(cold)))
        # In the APK, CT is used with the RGBW/CCT enable switch logic.
        # Ensure the CCT channel is enabled before applying CT values.
        # flags=0xE0 (RGB group on), light_mode=0x03 (CT), value=0x01 (CCT enabled)
        await self._write(packet_rgbw_status(0xE0, 0x03, 0x01))
        await self._write(packet_color_temperature(w, c))
        self.state.warm = w
        self.state.cold = c

    async def set_single_color(self, value: int) -> None:
        v = max(0, min(255, int(value)))
        await self._write(packet_single_color(v))
        self.state.single_color = v

    async def set_mode(self, mode: int) -> None:
        await self._write(packet_mode(mode))
        self.state.mode = mode & 0xFF

    async def set_mode_speed(self, speed: int) -> None:
        await self._write(packet_mode_speed(speed))
        self.state.mode_speed = max(0, min(255, int(speed)))

    async def set_scene(self, scene: int) -> None:
        await self._write(packet_scene(scene))
        self.state.scene = scene & 0xFF

    async def set_mic(
        self,
        on: bool | None = None,
        sensitivity: int | None = None,
        eq_mode: int | None = None,
    ) -> None:
        if on is not None:
            await self._write(packet_mic_onoff(on))
            self.state.mic_on = on
        if sensitivity is not None:
            await self._write(packet_mic_sensitivity(sensitivity))
            self.state.mic_sensitivity = int(sensitivity) & 0xFF
        if eq_mode is not None:
            await self._write(packet_mic_eq_mode(eq_mode))
            self.state.mic_eq_mode = int(eq_mode) & 0xFF
