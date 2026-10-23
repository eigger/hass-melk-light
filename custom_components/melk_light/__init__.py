"""The MELK Light Bar integration."""

from __future__ import annotations

from blesession.hass import radio_facts
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .melk_ble.device import MelkLedDevice

PLATFORMS: list[Platform] = [Platform.LIGHT, Platform.BINARY_SENSOR, Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up MELK Light Bar from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    address = entry.unique_id
    assert address is not None

    device = MelkLedDevice(address)
    device.report_facts = lambda trace: radio_facts(hass, address, trace.link)
    hass.data[DOMAIN][entry.entry_id] = {"address": address, "device": device}

    try:
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    except BaseException:
        await device.close()
        hass.data[DOMAIN].pop(entry.entry_id)
        raise

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    dev: MelkLedDevice = hass.data[DOMAIN][entry.entry_id]["device"]
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        await dev.close()
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
