"""Constants for MELK Light Bar integration."""

DOMAIN = "melk_light"
MANUFACTURER = "EasyLink / ELK BLE"

# Re-export BLE/protocol constants (kept in melk_ble)
from .melk_ble.constants import (  # noqa: E402
    CHARACTERISTIC_UUID,
    DEVICE_NAME_PREFIX,
    FOOTER,
    HEADER,
    PAD,
    SERVICE_UUID,
)
