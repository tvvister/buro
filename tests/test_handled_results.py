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
async def test_get_values(aiohttp_client):
    virtual_device = Mock(spec=DeviceBase)
    time_value = datetime(2020, 1, 1, 1, 1, 0)
    virtual_device.execute = AsyncMock(return_value=(time_value, 0.1))

    client = await aiohttp_client(create_app(virtual_device))
    resp = await client.get("/get_values/1")
    assert resp.status == 200
    content = await resp.content.read()

    assert (
        content
        == b'{"1": {"current": 0.1, "time": "2020-01-01 01:01:00", "voltage": 0.1}}'
    )


@pytest.mark.asyncio
async def test_start_channel(aiohttp_client):
    virtual_device = Mock(spec=DeviceBase)
    virtual_device.execute = AsyncMock(return_value=None)

    client = await aiohttp_client(create_app(virtual_device))
    resp = await client.post("/start_channel/1/34.4/343.34")
    assert resp.status == 200
    content = await resp.content.read()

    assert content == b"SUCCESS"


@pytest.mark.asyncio
async def test_disable_route(aiohttp_client):
    virtual_device = Mock(spec=DeviceBase)
    virtual_device.execute = AsyncMock(return_value=None)

    client = await aiohttp_client(create_app(virtual_device))
    resp = await client.post("/disable/1")
    assert resp.status == 200
    content = await resp.content.read()
    assert content == b"SUCCESS"
