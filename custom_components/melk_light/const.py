"""Constants for MELK Light Bar integration."""

from .melk_ble.constants import (
    CHARACTERISTIC_UUID,
    DEVICE_NAME_PREFIX,
    FOOTER,
    HEADER,
    PAD,
    SERVICE_UUID,
)

__all__ = [
    "CHARACTERISTIC_UUID",
    "DEVICE_NAME_PREFIX",
    "FOOTER",
    "HEADER",
    "PAD",
    "SERVICE_UUID",
]

DOMAIN = "melk_light"
MANUFACTURER = "EasyLink / ELK BLE"
