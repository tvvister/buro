import asyncio
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, Mock, patch

from driver_core.driver import DriverIml
from driver_core.virtual_device import VirtualDevice
from rest_api.rest_api_server import RestAPIServer


import asyncio
import time

import pytest

from aiohttp import web


# async def hello(request):
#     return web.Response(body=b"Hello, world")


# def create_app():
#     app = web.Application()
#     app.router.add_route("GET", "/", hello)
#     return app

# @pytest.mark.asyncio
# async def test_hello(aiohttp_client):
#     client = await aiohttp_client(create_app())
#     resp = await client.get("/")
#     assert resp.status == 200
#     text = await resp.text()
#     assert "Hello, world" in text

# @pytest.mark.asyncio
# async def test_coro(event_loop):
#     before = time.monotonic()
#     await asyncio.sleep(0.1, loop=event_loop)
#     after = time.monotonic()
#     assert after - before >= 0.1

def create_app(virtual_device):
    driver = DriverIml(virtual_device)
    server = RestAPIServer(driver)
    return server.app


@pytest.mark.asyncio
async def test_get_values_route(aiohttp_client):
    m = VirtualDevice()
    m.execute = AsyncMock(return_value=(None, 'Success'))
    
    client = await aiohttp_client(create_app(m))
    resp = await client.get("/get_values/ALL")
    assert resp.status == 200
    assert m.execute.called == True


# @pytest.fixture
# def cli(loop, aiohttp_client):
# @pytest.mark.asyncio
# async def test_get_values(cli):
#     resp = await cli.post('/', data={'value': 'foo'})
#     assert resp.status == 200
#     assert await resp.text() == 'thanks for the data'
#     assert cli.server.app['value'] == 'foo'
# async def test_get_value(cli):
#     cli.server.app['value'] = 'bar'
#     resp = await cli.get('/')
#     assert resp.status == 200
#     assert await resp.text() == 'value: bar'