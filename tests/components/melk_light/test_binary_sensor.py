"""Live connection diagnostics through HA and the external disconnect callback."""

import time
from unittest.mock import patch

from homeassistant.helpers import entity_registry as er


async def test_connection_and_normal_idle_disconnect(
    hass, mock_config_entry, mock_client
):
    mock_config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    registry = er.async_get(hass)
    entity_id = registry.async_get_entity_id(
        "binary_sensor", "melk_light", f"{mock_config_entry.unique_id}_connection"
    )
    assert hass.states.get(entity_id).state == "off"
    await hass.services.async_call(
        "light",
        "turn_on",
        {"entity_id": "light.melk_ccddeeff_light_bar"},
        blocking=True,
    )
    await hass.async_block_till_done()
    assert hass.states.get(entity_id).state == "on"
    device = hass.data["melk_light"][mock_config_entry.entry_id]["device"]
    last = device.reports.last
    device._idle_deadline = time.monotonic() - 1
    await device._auto_disconnect()
    await hass.async_block_till_done()
    assert hass.states.get(entity_id).state == "off"
    assert device.reports.failures == 0
    assert device.reports.last is last


async def test_unexpected_drop_updates_before_next_command(
    hass, mock_config_entry, mock_client
):
    mock_config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    with patch(
        "blesession.session.establish_connection", return_value=mock_client
    ) as connect:
        await hass.services.async_call(
            "light",
            "turn_on",
            {"entity_id": "light.melk_ccddeeff_light_bar"},
            blocking=True,
        )
        await hass.async_block_till_done()
    registry = er.async_get(hass)
    entity_id = registry.async_get_entity_id(
        "binary_sensor", "melk_light", f"{mock_config_entry.unique_id}_connection"
    )
    assert hass.states.get(entity_id).state == "on"
    # Some backends report is_connected=True briefly after their drop callback.
    connect.await_args.kwargs["disconnected_callback"](mock_client)
    await hass.async_block_till_done()
    assert hass.states.get(entity_id).state == "off"
