"""Real blesession with controlled external BLE transport."""

import asyncio
import time
from unittest.mock import AsyncMock, Mock, patch

import pytest
from bleak.backends.device import BLEDevice
from blesession import ConnectFailed, Unreachable

from custom_components.melk_light.melk_ble.device import MelkLedDevice
from custom_components.melk_light.melk_ble.protocol import packet_power


def route():
    return BLEDevice("AA:BB:CC:DD:EE:FF", "MELK-Test", {})


async def test_reuse_and_idle_disconnect(mock_client):
    dev = MelkLedDevice(route().address)
    with patch(
        "blesession.session.establish_connection", return_value=mock_client
    ) as connect:
        for _ in range(2):
            async with dev.connected(route):
                await dev.power(True)
        assert connect.await_count == 1
        assert mock_client.write_gatt_char.await_count == 4
        dev._idle_deadline = time.monotonic() - 1
        await dev._auto_disconnect()
        assert dev.client is None
        assert dev._disconnect_timer is None
        mock_client.disconnect.assert_awaited_once()


async def test_drop_between_repeats_refreshes_route(mock_client):
    dev = MelkLedDevice(route().address)
    resolve = Mock(side_effect=route)
    fresh = AsyncMock()
    fresh.is_connected = True

    async def drop(*args, **kwargs):
        mock_client.is_connected = False

    mock_client.write_gatt_char.side_effect = drop
    with patch(
        "blesession.session.establish_connection", side_effect=[mock_client, fresh]
    ) as connect:
        async with dev.connected(resolve):
            await dev.power(True)
        assert connect.await_count == 2
        assert resolve.call_count == 3
        assert fresh.write_gatt_char.await_args.args[1] == packet_power(True)
    await dev.close()


async def test_command_blocks_do_not_interleave(mock_client):
    dev = MelkLedDevice(route().address)
    started, release = asyncio.Event(), asyncio.Event()
    order = []

    async def first():
        async with dev.connected(route):
            order.append("first-start")
            started.set()
            await release.wait()
            await dev.power(True)
            order.append("first-end")

    async def second():
        await started.wait()
        async with dev.connected(route):
            order.append("second")
            await dev.power(False)

    a, b = asyncio.create_task(first()), asyncio.create_task(second())
    await started.wait()
    await asyncio.sleep(0)
    assert order == ["first-start"]
    # An old idle task must not disconnect a later command after waiting.
    dev._idle_deadline = time.monotonic() - 1
    idle = asyncio.create_task(dev._auto_disconnect())
    release.set()
    await asyncio.gather(a, b, idle)
    assert order == ["first-start", "first-end", "second"]
    assert dev.client is mock_client
    await dev.close()


async def test_cancel_releases_connection_and_lock(mock_client):
    dev = MelkLedDevice(route().address)
    started = asyncio.Event()

    async def command():
        async with dev.connected(route):
            started.set()
            await asyncio.Event().wait()

    task = asyncio.create_task(command())
    await started.wait()
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert not dev._lock.locked()
    assert dev.client is None
    mock_client.disconnect.assert_awaited_once()
    await dev.close()
    with pytest.raises(RuntimeError, match="unloaded"):
        async with dev.connected(route):
            pass


@pytest.mark.parametrize("failure", [Unreachable("test"), OSError("radio failed")])
async def test_lookup_failure_does_not_update_state(mock_client, failure):
    dev = MelkLedDevice(route().address)
    with pytest.raises(type(failure)):
        async with dev.connected(Mock(side_effect=failure)):
            await dev.power(True)
    assert dev.state.is_on is False
    await dev.close()


async def test_connect_failure_recoverable(mock_client):
    dev = MelkLedDevice(route().address)
    with patch(
        "blesession.session.establish_connection", side_effect=OSError("cannot connect")
    ):
        with pytest.raises(ConnectFailed):
            async with dev.connected(route):
                await dev.power(True)
    async with dev.connected(route):
        await dev.power(True)
    assert dev.state.is_on
    await dev.close()


async def test_cancel_during_settle_closes_unhanded_client(mock_client):
    dev = MelkLedDevice(route().address)
    settling = asyncio.Event()

    async def settle(*args):
        settling.set()
        await asyncio.Event().wait()

    async def command():
        async with dev.connected(route):
            await dev.power(True)

    with (
        patch("custom_components.melk_light.melk_ble.device._POST_CONNECT_DELAY", 0.3),
        patch("blesession.session._settle", side_effect=settle),
    ):
        task = asyncio.create_task(command())
        await settling.wait()
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
    mock_client.disconnect.assert_awaited_once()
    assert dev.client is None
    assert dev._disconnect_timer is None
    assert not dev._lock.locked()


async def test_disconnect_timeout_is_bounded(mock_client):
    dev = MelkLedDevice(route().address)
    async with dev.connected(route):
        await dev.power(True)
    mock_client.disconnect.side_effect = TimeoutError("proxy unavailable")
    await dev.close()
    assert dev.client is None
    assert dev._disconnect_timer is None
