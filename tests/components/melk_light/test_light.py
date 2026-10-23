"""Services run through the real HA light platform and actual protocol."""

import pytest
from homeassistant.exceptions import HomeAssistantError

from custom_components.melk_light.melk_ble.protocol import (
    packet_brightness,
    packet_color,
    packet_power,
)


async def test_light_commands(hass, mock_config_entry, mock_client):
    mock_config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    entity_id = "light.melk_ccddeeff_light_bar"
    await hass.services.async_call(
        "light",
        "turn_on",
        {
            "entity_id": entity_id,
            "brightness": 128,
            "rgb_color": [10, 20, 30],
            "effect": "Sunrise",
        },
        blocking=True,
    )
    state = hass.states.get(entity_id)
    assert state.state == "on"
    assert state.attributes["brightness"] == 128
    assert state.attributes["rgb_color"] == (10, 20, 30)
    calls = mock_client.write_gatt_char.await_args_list
    assert [c.args[1] for c in calls[:6]] == [packet_power(True)] * 2 + [
        packet_brightness(128)
    ] * 2 + [packet_color(10, 20, 30)] * 2
    assert all(c.kwargs == {"response": False} for c in calls)
    await hass.services.async_call(
        "light", "turn_off", {"entity_id": entity_id}, blocking=True
    )
    assert hass.states.get(entity_id).state == "off"
    assert mock_client.write_gatt_char.await_args.args[1] == packet_power(False)


async def test_failure_does_not_claim_success_and_recovers(
    hass, mock_config_entry, mock_client
):
    mock_config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    mock_client.write_gatt_char.side_effect = OSError("radio lost")
    with pytest.raises(HomeAssistantError):
        await hass.services.async_call(
            "light",
            "turn_on",
            {"entity_id": "light.melk_ccddeeff_light_bar"},
            blocking=True,
        )
    assert hass.states.get("light.melk_ccddeeff_light_bar").state == "off"
    mock_client.write_gatt_char.side_effect = None
    await hass.services.async_call(
        "light",
        "turn_on",
        {"entity_id": "light.melk_ccddeeff_light_bar"},
        blocking=True,
    )
    assert hass.states.get("light.melk_ccddeeff_light_bar").state == "on"
