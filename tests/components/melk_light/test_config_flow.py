"""Configuration through the real HA flow manager."""

from unittest.mock import patch

from homeassistant.components.bluetooth import BluetoothServiceInfoBleak
from homeassistant.data_entry_flow import FlowResultType


def discovery(name="MELK-Test"):
    return BluetoothServiceInfoBleak(
        name=name,
        address="AA:BB:CC:DD:EE:FF",
        rssi=-60,
        manufacturer_data={},
        service_data={},
        service_uuids=[],
        source="test",
        device=None,
        advertisement=None,
        connectable=True,
        time=0,
        tx_power=None,
    )


async def test_bluetooth_confirm_and_duplicate(hass, mock_client):
    with patch(
        "homeassistant.components.onboarding.async_is_onboarded", return_value=True
    ):
        result = await hass.config_entries.flow.async_init(
            "melk_light", context={"source": "bluetooth"}, data=discovery()
        )
    assert result["type"] is FlowResultType.FORM
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {})
    assert result["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
    result = await hass.config_entries.flow.async_init(
        "melk_light", context={"source": "bluetooth"}, data=discovery()
    )
    assert result["reason"] == "already_configured"


async def test_unsupported(hass):
    result = await hass.config_entries.flow.async_init(
        "melk_light", context={"source": "bluetooth"}, data=discovery("Other")
    )
    assert result["reason"] == "not_supported"


async def test_user_empty(hass):
    with patch(
        "custom_components.melk_light.config_flow.async_discovered_service_info",
        return_value=[],
    ):
        result = await hass.config_entries.flow.async_init(
            "melk_light", context={"source": "user"}
        )
    assert result["reason"] == "no_devices_found"


async def test_user_selection(hass, mock_client):
    with patch(
        "custom_components.melk_light.config_flow.async_discovered_service_info",
        return_value=[discovery()],
    ):
        result = await hass.config_entries.flow.async_init(
            "melk_light", context={"source": "user"}
        )
    assert result["type"] is FlowResultType.FORM
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {"address": "AA:BB:CC:DD:EE:FF"}
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
