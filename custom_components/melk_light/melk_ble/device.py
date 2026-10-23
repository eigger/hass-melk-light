"""MELK protocol state and serialized, reusable BLE sessions."""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import Callable
from contextlib import asynccontextmanager
from dataclasses import dataclass

from bleak import BleakClient
from bleak.backends.device import BLEDevice
from blesession import ble_session, still_up

from .constants import CHARACTERISTIC_UUID, DEVICE_NAME_PREFIX
from .protocol import (
    packet_brightness,
    packet_color,
    packet_color_temperature,
    packet_mic_eq_mode,
    packet_mic_onoff,
    packet_mic_sensitivity,
    packet_mode,
    packet_mode_speed,
    packet_power,
    packet_rgbw_status,
    packet_scene,
    packet_single_color,
)

_LOGGER = logging.getLogger(__name__)
_WRITE_REPEAT_COUNT = 2
_WRITE_REPEAT_DELAY = 0.1
_POST_CONNECT_DELAY = 0.3
_DISCONNECT_TIMEOUT = 30.0


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
    """Own MELK commands; blesession owns opening and reusing each link."""

    def __init__(self, address: str) -> None:
        self.address = address
        self.client: BleakClient | None = None
        self.name: str | None = None
        self.state = MelkState()
        self._lock = asyncio.Lock()
        self._resolve_device: Callable[[], BLEDevice] | None = None
        self._last_tx = 0.0
        self._idle_deadline = 0.0
        self._disconnect_timer: asyncio.TimerHandle | None = None
        self._closed = False

    def _cancel_timer(self) -> None:
        if self._disconnect_timer is not None:
            self._disconnect_timer.cancel()
            self._disconnect_timer = None

    def _reset_disconnect_timer(self) -> None:
        self._cancel_timer()
        self._idle_deadline = time.monotonic() + _DISCONNECT_TIMEOUT
        self._disconnect_timer = asyncio.get_running_loop().call_later(
            _DISCONNECT_TIMEOUT, lambda: asyncio.create_task(self._auto_disconnect())
        )

    async def _auto_disconnect(self) -> None:
        async with self._lock:
            # A command may have refreshed the deadline while this task waited.
            if time.monotonic() >= self._idle_deadline:
                await self._disconnect_locked()

    def is_connected(self) -> bool:
        return still_up(self.client)

    async def _ensure_client(self) -> BleakClient:
        assert self._resolve_device is not None
        ble_device = self._resolve_device()
        async with ble_session(
            ble_device, client=self.client, keep=True, settle_s=_POST_CONNECT_DELAY
        ) as client:
            self.client = client
            self.name = ble_device.name or DEVICE_NAME_PREFIX.rstrip("-")
            return client

    async def _disconnect_locked(self) -> None:
        self._cancel_timer()
        client, self.client = self.client, None
        if client is not None and client.is_connected:
            try:
                # keep=True hands ownership of idle cleanup to this device.
                async with asyncio.timeout(10):
                    await client.disconnect()
            except Exception as err:
                _LOGGER.debug("MELK disconnect failed: %s", err)

    async def disconnect(self) -> None:
        """Disconnect after any active command block finishes."""
        async with self._lock:
            await self._disconnect_locked()

    async def close(self) -> None:
        """Stop accepting commands and release resources on unload."""
        self._closed = True
        await self.disconnect()

    async def _write(self, data: bytes) -> None:
        """Repeat write-without-response packets with the device's 100 ms gap.

        The connected context holds the lock for the whole command sequence.
        Resolve the current HA route again if a link drops between repeats.
        """
        gap = time.monotonic() - self._last_tx
        if gap < _WRITE_REPEAT_DELAY:
            await asyncio.sleep(_WRITE_REPEAT_DELAY - gap)
        for n in range(_WRITE_REPEAT_COUNT):
            client = await self._ensure_client()
            self._last_tx = time.monotonic()
            await client.write_gatt_char(CHARACTERISTIC_UUID, data, response=False)
            if n + 1 < _WRITE_REPEAT_COUNT:
                await asyncio.sleep(_WRITE_REPEAT_DELAY)

    @asynccontextmanager
    async def connected(self, resolve_device: Callable[[], BLEDevice]):
        """Serialize a complete command and resolve its route under the lock."""
        async with self._lock:
            if self._closed:
                raise RuntimeError("MELK device is unloaded")
            self._cancel_timer()
            self._resolve_device = resolve_device
            try:
                await self._ensure_client()
                yield
            except BaseException:
                await self._disconnect_locked()
                raise
            finally:
                self._resolve_device = None
                if self._closed or self.client is None:
                    await self._disconnect_locked()
                else:
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
