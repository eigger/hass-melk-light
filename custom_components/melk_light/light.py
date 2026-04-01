"""Light platform for MELK Light Bar."""

from __future__ import annotations

import logging

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_RGB_COLOR,
    ColorMode,
    LightEntity,
    LightEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN
from .entity import MelkBaseEntity
from .effects import MELK_EFFECTS, effect_name_from_mode
from .melk_ble.device import MelkLedDevice

_LOGGER = logging.getLogger(__name__)

_MODE_EFFECTS = sorted(MELK_EFFECTS.keys(), key=lambda s: s.lower())


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    dev: MelkLedDevice = hass.data[DOMAIN][entry.entry_id]["device"]
    async_add_entities([MelkLightEntity(hass, entry, dev)])


class MelkLightEntity(MelkBaseEntity, LightEntity):
    _attr_name = "Light Bar"
    _attr_supported_color_modes = {ColorMode.RGB}
    _attr_color_mode = ColorMode.RGB
    _attr_supported_features = LightEntityFeature.EFFECT
    _attr_effect_list = _MODE_EFFECTS

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, dev: MelkLedDevice) -> None:
        super().__init__(hass, entry, dev)
        self._attr_unique_id = entry.unique_id

        self._attr_is_on = dev.state.is_on
        self._attr_brightness = dev.state.brightness
        self._attr_rgb_color = dev.state.rgb
        self._attr_effect = effect_name_from_mode(dev.state.mode)

    @property
    def available(self) -> bool:
        return True

    @property
    def extra_state_attributes(self) -> dict:
        st = self._dev.state
        attrs: dict = {}
        if st.mode is not None:
            attrs["mode"] = st.mode
        if st.mode_speed is not None:
            attrs["mode_speed"] = st.mode_speed
        if st.scene is not None:
            attrs["scene"] = st.scene
        return attrs

    async def async_turn_on(self, **kwargs) -> None:
        ble_device = self._get_ble_device()
        if not ble_device:
            _LOGGER.warning("BLE device not available for %s", self._entry.unique_id)
            return

        self._attr_is_on = True
        if ATTR_BRIGHTNESS in kwargs:
            self._attr_brightness = int(kwargs[ATTR_BRIGHTNESS])
        if ATTR_RGB_COLOR in kwargs:
            r, g, b = kwargs[ATTR_RGB_COLOR]
            self._attr_rgb_color = (int(r), int(g), int(b))
        if "effect" in kwargs and kwargs["effect"] is not None:
            eff = str(kwargs["effect"])
            if eff in MELK_EFFECTS:
                self._attr_effect = eff
        self.async_write_ha_state()

        try:
            async with self._dev.connected(ble_device):
                # Always send power(True) first so the device is guaranteed to
                # be on before we apply color/brightness.  Cached state may be
                # stale (e.g. device was physically switched off).
                await self._dev.power(True)

                if ATTR_BRIGHTNESS in kwargs:
                    await self._dev.set_brightness(kwargs[ATTR_BRIGHTNESS])
                    self._attr_brightness = self._dev.state.brightness

                if ATTR_RGB_COLOR in kwargs:
                    r, g, b = kwargs[ATTR_RGB_COLOR]
                    await self._dev.set_rgb(r, g, b)
                    self._attr_rgb_color = self._dev.state.rgb

                if "effect" in kwargs and kwargs["effect"] is not None:
                    eff = str(kwargs["effect"])
                    if eff in MELK_EFFECTS:
                        await self._dev.set_mode(MELK_EFFECTS[eff])
                        self._attr_effect = eff
        except Exception:
            _LOGGER.exception("BLE command failed for %s", self._entry.unique_id)
        finally:
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:  # noqa: ARG002
        ble_device = self._get_ble_device()
        if not ble_device:
            _LOGGER.warning("BLE device not available for %s", self._entry.unique_id)
            return

        self._attr_is_on = False
        self.async_write_ha_state()

        try:
            async with self._dev.connected(ble_device):
                await self._dev.power(False)
        except Exception:
            _LOGGER.exception("BLE command failed for %s", self._entry.unique_id)
        finally:
            self.async_write_ha_state()
