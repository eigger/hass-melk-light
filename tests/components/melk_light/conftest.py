"""Fixtures for the example integration."""

# <!-- hass-standards:domain-fixtures:start -->
# Use pytest_homeassistant_custom_component.common.MockConfigEntry for
# mock_config_entry when the integration uses config entries.
# Define mock_client only when an external communication client is present.
# Mock external communication boundaries, never Home Assistant core modules.
# Keep integration-specific fixtures below this managed block.
# <!-- hass-standards:domain-fixtures:end -->

from unittest.mock import AsyncMock, patch

import pytest
from bleak import BleakClient
from bleak.backends.device import BLEDevice
from pytest_homeassistant_custom_component.common import MockConfigEntry


@pytest.fixture(autouse=True)
def mock_radio_management(mock_bluetooth):
    """The minimum HA plugin predates habluetooth's BlueZ channel import.

    Replace only the hardware management socket setup, as the plugin does
    for its original import path. The HA Bluetooth manager still runs.
    """
    with patch(
        "habluetooth.channels.bluez.MGMTBluetoothCtl.setup", new_callable=AsyncMock
    ):
        yield


@pytest.fixture
def mock_config_entry():
    return MockConfigEntry(
        domain="melk_light", title="MELK-Test", unique_id="AA:BB:CC:DD:EE:FF", data={}
    )


@pytest.fixture
def mock_client():
    """Replace only the radio/connection boundary; keep real blesession."""
    client = AsyncMock(spec=BleakClient)
    client.is_connected = True
    device = BLEDevice("AA:BB:CC:DD:EE:FF", "MELK-Test", {})
    with (
        patch("blesession.session.establish_connection", return_value=client),
        patch("blesession.hass.ble_device_or_raise", return_value=device),
        patch("custom_components.melk_light.melk_ble.device._POST_CONNECT_DELAY", 0),
        patch("custom_components.melk_light.melk_ble.device._WRITE_REPEAT_DELAY", 0),
    ):
        yield client
