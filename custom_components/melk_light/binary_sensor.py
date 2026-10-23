"""Live BLE connection status; no polling or extra connections."""

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import MelkBaseEntity
from .melk_ble.device import MelkLedDevice


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    device = hass.data[DOMAIN][entry.entry_id]["device"]
    async_add_entities([MelkConnectionSensor(hass, entry, device)])


class MelkConnectionSensor(MelkBaseEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_translation_key = "connection"
    _attr_should_poll = False

    def __init__(
        self, hass: HomeAssistant, entry: ConfigEntry, device: MelkLedDevice
    ) -> None:
        super().__init__(hass, entry, device)
        self._attr_unique_id = f"{entry.unique_id}_connection"

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        self.async_on_remove(
            self._dev.add_connection_listener(self.schedule_update_ha_state)
        )

    @property
    def is_on(self) -> bool:
        return self._dev.is_connected()
