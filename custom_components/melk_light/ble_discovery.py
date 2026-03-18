"""Home Assistant specific BLE discovery helpers for MELK LED bar."""

from __future__ import annotations

from bluetooth_sensor_state_data import BluetoothData
from home_assistant_bluetooth import BluetoothServiceInfoBleak

from .melk_ble.constants import DEVICE_NAME_PREFIX, SERVICE_UUID


class MelkBluetoothDeviceData(BluetoothData):
    """Bluetooth device matcher for MELK LED bar (HA discovery)."""

    DEVICE_NAME_PREFIX = DEVICE_NAME_PREFIX
    SERVICE_UUID = SERVICE_UUID

    def __init__(self) -> None:
        super().__init__()
        self.last_service_info: BluetoothServiceInfoBleak | None = None

    def supported(self, data: BluetoothServiceInfoBleak) -> bool:
        if not data.name or not data.name.startswith(self.DEVICE_NAME_PREFIX):
            return False
        # Some proxies may not expose service UUIDs; keep this permissive.
        if data.service_uuids:
            if self.SERVICE_UUID.lower() not in [u.lower() for u in data.service_uuids]:
                return False
        self.last_service_info = data
        return True

