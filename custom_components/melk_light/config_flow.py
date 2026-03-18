"""Config flow for MELK Light Bar integration."""

from __future__ import annotations

from collections.abc import Mapping
import dataclasses
from typing import Any

import voluptuous as vol

from homeassistant.components import onboarding
from homeassistant.components.bluetooth import (
    BluetoothServiceInfoBleak,
    async_discovered_service_info,
)
from homeassistant.config_entries import (
    SOURCE_REAUTH,
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
)
from homeassistant.const import CONF_ADDRESS
from homeassistant.core import callback

from .const import DOMAIN
from .ble_discovery import MelkBluetoothDeviceData as DeviceData


@dataclasses.dataclass
class Discovery:
    """A discovered bluetooth device."""

    title: str
    discovery_info: BluetoothServiceInfoBleak
    device: DeviceData


def _title(discovery_info: BluetoothServiceInfoBleak) -> str:
    return discovery_info.name


class MelkLightConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MELK Light Bar."""

    VERSION = 1

    def __init__(self) -> None:
        self._discovery_info: BluetoothServiceInfoBleak | None = None
        self._discovered_device: DeviceData | None = None
        self._discovered_devices: dict[str, Discovery] = {}

    async def async_step_bluetooth(
        self, discovery_info: BluetoothServiceInfoBleak
    ) -> ConfigFlowResult:
        """Handle discovery via bluetooth."""
        await self.async_set_unique_id(discovery_info.address)
        self._abort_if_unique_id_configured()

        device = DeviceData()
        if not device.supported(discovery_info):
            return self.async_abort(reason="not_supported")

        title = _title(discovery_info)
        self.context["title_placeholders"] = {"name": title}
        self._discovery_info = discovery_info
        self._discovered_device = device

        return await self.async_step_bluetooth_confirm()

    async def async_step_bluetooth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Confirm discovery."""
        if user_input is not None or not onboarding.async_is_onboarded(self.hass):
            return self._async_get_or_create_entry()

        self._set_confirm_only()
        return self.async_show_form(
            step_id="bluetooth_confirm",
            description_placeholders=self.context["title_placeholders"],
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Let user pick a discovered device."""
        if user_input is not None:
            address = user_input[CONF_ADDRESS]
            await self.async_set_unique_id(address, raise_on_progress=False)
            self._abort_if_unique_id_configured()
            discovery = self._discovered_devices[address]

            self.context["title_placeholders"] = {"name": discovery.title}
            self._discovery_info = discovery.discovery_info
            self._discovered_device = discovery.device
            return self._async_get_or_create_entry()

        current_addresses = self._async_current_ids(include_ignore=False)
        for discovery_info in async_discovered_service_info(self.hass):
            address = discovery_info.address
            if address in current_addresses or address in self._discovered_devices:
                continue
            device = DeviceData()
            if device.supported(discovery_info):
                self._discovered_devices[address] = Discovery(
                    title=_title(discovery_info),
                    discovery_info=discovery_info,
                    device=device,
                )

        if not self._discovered_devices:
            return self.async_abort(reason="no_devices_found")

        titles = {
            address: discovery.title
            for (address, discovery) in self._discovered_devices.items()
        }
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_ADDRESS): vol.In(titles)}),
        )

    async def async_step_reauth(
        self, entry_data: Mapping[str, Any]
    ) -> ConfigFlowResult:
        """Handle a flow initialized by a reauth event."""
        device: DeviceData = entry_data["device"]
        self._discovered_device = device
        self._discovery_info = device.last_service_info
        return self.async_abort(reason="reauth_successful")

    @callback
    def _async_get_or_create_entry(self) -> ConfigFlowResult:
        """Create the config entry."""
        if self.source == SOURCE_REAUTH:
            return self.async_update_reload_and_abort(self._get_reauth_entry(), data={})

        return self.async_create_entry(
            title=self.context["title_placeholders"]["name"],
            data={},
        )

