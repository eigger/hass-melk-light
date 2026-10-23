"""Real HA config-entry and platform lifecycle coverage."""

from unittest.mock import patch

from homeassistant.config_entries import ConfigEntryState


async def test_setup_unload_reload(hass, mock_config_entry, mock_client):
    mock_config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    assert mock_config_entry.state is ConfigEntryState.LOADED
    assert hass.states.get("light.melk_ccddeeff_light_bar") is not None
    device = hass.data["melk_light"][mock_config_entry.entry_id]["device"]
    await hass.services.async_call(
        "light",
        "turn_on",
        {"entity_id": "light.melk_ccddeeff_light_bar"},
        blocking=True,
    )
    assert device._disconnect_timer is not None
    assert await hass.config_entries.async_unload(mock_config_entry.entry_id)
    assert device._closed
    assert device.client is None
    assert device._disconnect_timer is None
    mock_client.disconnect.assert_awaited_once()
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    assert hass.data["melk_light"][mock_config_entry.entry_id]["device"] is not device


async def test_setup_failure_cleans_device(hass, mock_config_entry, mock_client):
    mock_config_entry.add_to_hass(hass)
    with patch(
        "homeassistant.config_entries.ConfigEntries.async_forward_entry_setups",
        side_effect=RuntimeError("platform failure"),
    ):
        assert not await hass.config_entries.async_setup(mock_config_entry.entry_id)
    assert mock_config_entry.entry_id not in hass.data["melk_light"]


async def test_failed_unload_keeps_device(hass, mock_config_entry, mock_client):
    mock_config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    with patch(
        "homeassistant.config_entries.ConfigEntries.async_unload_platforms",
        return_value=False,
    ):
        assert not await hass.config_entries.async_unload(mock_config_entry.entry_id)
    assert not hass.data["melk_light"][mock_config_entry.entry_id]["device"]._closed
