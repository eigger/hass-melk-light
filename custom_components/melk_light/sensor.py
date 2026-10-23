"""Diagnostic sensors backed by blesession's retained reports."""

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import MelkBaseEntity
from .melk_ble.device import MelkLedDevice

SENSORS = (
    SensorEntityDescription(
        key="duration",
        translation_key="duration",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="last_failure",
        translation_key="last_failure",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="error_count",
        translation_key="error_count",
        icon="mdi:alert-circle-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    device = hass.data[DOMAIN][entry.entry_id]["device"]
    async_add_entities(MelkReportSensor(hass, entry, device, desc) for desc in SENSORS)


class MelkReportSensor(MelkBaseEntity, SensorEntity):
    """Expose last session, retained failure and reload-scoped failure count."""

    _attr_should_poll = False

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        device: MelkLedDevice,
        description: SensorEntityDescription,
    ) -> None:
        super().__init__(hass, entry, device)
        self.entity_description = description
        self._attr_unique_id = f"{entry.unique_id}_{description.key}"

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        self.async_on_remove(self._dev.reports.add_listener(self.async_write_ha_state))

    @property
    def native_value(self):
        reports = self._dev.reports
        if self.entity_description.key == "error_count":
            return reports.failures
        if self.entity_description.key == "last_failure":
            return reports.last_failure_at
        return reports.last.get("duration_s") if reports.last else None

    @property
    def extra_state_attributes(self) -> dict | None:
        reports = self._dev.reports
        if self.entity_description.key == "last_failure":
            return reports.last_failure
        if self.entity_description.key == "duration":
            return reports.last
        return None
