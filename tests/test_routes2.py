from unittest.mock import Mock
import pytest
from aiohttp import web
from driver_core.driver import DeviceBase, DriverIml
from rest_api.rest_api_server import RestAPIServer

@pytest.fixture
def cli(loop, aiohttp_client):
    mock_device =  Mock(spec=DeviceBase)
    driver = DriverIml(mock_device)
    server = RestAPIServer(driver)
    server.start()
    return loop.run_until_complete(aiohttp_client(server.app))

async def test_set_value(cli):
    resp = await cli.post('/', data={'value': 'foo'})
    assert resp.status == 200
    assert await resp.text() == 'thanks for the data'
    assert cli.server.app['value'] == 'foo'

async def test_get_value(cli):
    cli.server.app['value'] = 'bar'
    resp = await cli.get('/')
    assert resp.status == 200
    assert await resp.text() == 'value: bar'