"""Real HA diagnostic entities and retained blesession reports."""

from unittest.mock import patch

import pytest
from blesession import Unreachable
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import entity_registry as er


async def setup(hass, entry):
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    registry = er.async_get(hass)
    ids = {
        key: registry.async_get_entity_id(
            "sensor", "melk_light", f"{entry.unique_id}_{key}"
        )
        for key in ("duration", "last_failure", "error_count")
    }
    return hass.data["melk_light"][entry.entry_id]["device"], ids


async def command(hass):
    await hass.services.async_call(
        "light",
        "turn_on",
        {"entity_id": "light.melk_ccddeeff_light_bar"},
        blocking=True,
    )
    await hass.async_block_till_done()


async def test_initial_and_successful_command(hass, mock_config_entry, mock_client):
    device, ids = await setup(hass, mock_config_entry)
    assert hass.states.get(ids["duration"]).state == "unknown"
    assert hass.states.get(ids["last_failure"]).state == "unknown"
    assert hass.states.get(ids["error_count"]).state == "0"
    mock_client.write_gatt_char.assert_not_awaited()
    await command(hass)
    duration = hass.states.get(ids["duration"])
    assert float(duration.state) >= 0
    assert duration.attributes["success"] is True
    assert duration.attributes["operation"] == "turn_on"
    assert "connect_s" in duration.attributes
    assert "transfer_s" in duration.attributes
    assert hass.states.get(ids["error_count"]).state == "0"
    assert device.reports.last_failure is None
    registry = er.async_get(hass)
    light_device = registry.async_get("light.melk_ccddeeff_light_bar").device_id
    assert all(
        registry.async_get(entity_id).device_id == light_device
        for entity_id in ids.values()
    )
    assert all(
        registry.async_get(entity_id).entity_category.value == "diagnostic"
        for entity_id in ids.values()
    )


async def test_failure_persists_after_recovery(hass, mock_config_entry, mock_client):
    device, ids = await setup(hass, mock_config_entry)
    mock_client.write_gatt_char.side_effect = OSError(
        f"link failed {mock_config_entry.unique_id}"
    )
    with pytest.raises(HomeAssistantError):
        await command(hass)
    await hass.async_block_till_done()
    failure = hass.states.get(ids["last_failure"])
    assert failure.state != "unknown"
    assert failure.attributes["failed_stage"] == "transfer"
    assert failure.attributes["success"] is False
    assert mock_config_entry.unique_id not in str(failure.attributes)
    assert hass.states.get(ids["error_count"]).state == "1"
    mock_client.write_gatt_char.side_effect = None
    await command(hass)
    assert hass.states.get(ids["duration"]).attributes["success"] is True
    assert hass.states.get(ids["last_failure"]).state == failure.state
    assert hass.states.get(ids["last_failure"]).attributes == failure.attributes
    assert hass.states.get(ids["error_count"]).state == "1"
    assert device.reports.last_failure is not device.reports.last


async def test_unreachable_is_recorded(hass, mock_config_entry, mock_client):
    _, ids = await setup(hass, mock_config_entry)
    with patch(
        "custom_components.melk_light.entity.ble_device_or_raise",
        side_effect=Unreachable("test"),
    ):
        with pytest.raises(HomeAssistantError):
            await command(hass)
    await hass.async_block_till_done()
    assert (
        hass.states.get(ids["last_failure"]).attributes["failed_stage"] == "unreachable"
    )
    assert hass.states.get(ids["error_count"]).state == "1"


async def test_unload_removes_listeners_and_reload_resets_count(
    hass, mock_config_entry, mock_client
):
    device, ids = await setup(hass, mock_config_entry)
    mock_client.write_gatt_char.side_effect = OSError("write failed")
    with pytest.raises(HomeAssistantError):
        await command(hass)
    assert await hass.config_entries.async_unload(mock_config_entry.entry_id)
    assert device.reports._listeners == []
    assert device._connection_listeners == []
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    assert hass.states.get(ids["error_count"]).state == "0"
    assert hass.states.get(ids["last_failure"]).state == "unknown"
