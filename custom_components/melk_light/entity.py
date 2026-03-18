"""Shared entity helpers for MELK Light Bar."""

from __future__ import annotations

from homeassistant.components import bluetooth
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN, MANUFACTURER
from .melk_ble.device import MelkLedDevice


class MelkBaseEntity:
    """Common bits for MELK entities."""

    _attr_has_entity_name = True

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, dev: MelkLedDevice) -> None:
        self.hass = hass
        self._entry = entry
        self._dev = dev

        identifier = (entry.unique_id or "").replace(":", "")[-8:]
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.unique_id)},
            name=dev.name or f"MELK {identifier}",
            manufacturer=MANUFACTURER,
            model="MELK LED Bar",
        )

    def _get_ble_device(self):
        return bluetooth.async_ble_device_from_address(self.hass, self._entry.unique_id)

