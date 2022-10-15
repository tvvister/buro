from datetime import datetime
from unittest.mock import AsyncMock

from driver_core.driver import DriverIml
from driver_core.virtual_device import VirtualDevice
from rest_api.rest_api_server import RestAPIServer

import pytest


def create_app(virtual_device):
    driver = DriverIml(virtual_device)
    server = RestAPIServer(driver)
    return server.app


@pytest.mark.asyncio
async def test_get_values_correctness(aiohttp_client):
    virtual_device = VirtualDevice()
    virtual_device.execute = AsyncMock(
        return_value=(datetime.now(), 'Success'))

    client = await aiohttp_client(create_app(virtual_device))
    resp = await client.get("/get_values/ALL")
    assert resp.status == 200
    assert virtual_device.execute.called == True
    assert len(virtual_device.execute.mock_calls) == 8


@pytest.mark.asyncio
async def test_start_channel_correctness(aiohttp_client):
    virtual_device = VirtualDevice()
    virtual_device.execute = AsyncMock(return_value=None)

    client = await aiohttp_client(create_app(virtual_device))
    resp = await client.post("/start_channel/1/34.4/343.34")
    assert resp.status == 200

    expected = [':SOURce1:CURRent 34.4',
                ':SOURce1:VOLTage 343.34', ':OUTPut1:STATe ON']
    for call, exp in zip(virtual_device.execute.await_args_list, expected):
        assert call.args[0] == exp


@pytest.mark.asyncio
async def test_disable_route(aiohttp_client):
    virtual_device = VirtualDevice()
    virtual_device.execute = AsyncMock(return_value=None)

    client = await aiohttp_client(create_app(virtual_device))
    resp = await client.post("/disable/1")
    assert resp.status == 200
    expected = ':OUTPut1:STATe OFF'

    assert virtual_device.execute.await_args_list[0].args[0] == expected
