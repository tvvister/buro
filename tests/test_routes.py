from datetime import datetime
from unittest.mock import AsyncMock, Mock
import pytest

from driver_core.driver import DeviceBase, DriverIml
from rest_api.rest_api_server import RestAPIServer


def create_app(virtual_device):
    driver = DriverIml(virtual_device)
    server = RestAPIServer(driver)
    return server.app


@pytest.mark.asyncio
async def test_get_values_route(aiohttp_client):
    virtual_device = Mock(spec=DeviceBase)
    virtual_device.execute = AsyncMock(return_value=(datetime.now(), "Success"))

    client = await aiohttp_client(create_app(virtual_device))
    resp = await client.get("/get_values/ALL")
    assert resp.status == 200
    assert virtual_device.execute.called == True
    assert len(virtual_device.execute.mock_calls) == 8


@pytest.mark.asyncio
async def test_start_channel_route(aiohttp_client):
    virtual_device = Mock(spec=DeviceBase)
    virtual_device.execute = AsyncMock(return_value=None)

    client = await aiohttp_client(create_app(virtual_device))
    resp = await client.post("/start_channel/1/34.4/343.34")
    assert resp.status == 200
    assert virtual_device.execute.called == True
    assert len(virtual_device.execute.mock_calls) == 3


@pytest.mark.asyncio
async def test_disable_route(aiohttp_client):
    virtual_device = Mock(spec=DeviceBase)
    virtual_device.execute = AsyncMock(return_value=None)

    client = await aiohttp_client(create_app(virtual_device))
    resp = await client.post("/disable/1")
    assert resp.status == 200
    assert virtual_device.execute.called == True
    assert len(virtual_device.execute.mock_calls) == 1
