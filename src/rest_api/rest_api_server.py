import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from aiohttp import web
from datetime import datetime
import json

from driver_core.driver import DriverBase


def default_json(obj):
    if isinstance(obj, datetime):
        return str(obj)
    raise TypeError("Unable to serialize {!r}".format(obj))


def start_log(driver):
    asyncio.run(driver.start_log())


class RestAPIServer:
    def __init__(self, driver):
        assert isinstance(
            driver, DriverBase
        ), "<device> arg must be a type which is derived from DeviceBase"
        self._driver = driver
        self.app = web.Application()
        self.app.router.add_post(
            "/start_channel/{channel:\d+}/{current:.*}/{voltage:.*}", self.start_channel
        )
        self.app.router.add_post("/disable/{channel:\d+}", self.disable)
        self.app.router.add_get("/get_values/{channel_info:.*}", self.get_values)

    async def start_channel(self, request):
        current = float(request.match_info.get("current"))
        voltage = float(request.match_info.get("voltage"))
        channel = int(request.match_info.get("channel"))
        try:
            resp = await self._driver.start_channel(channel, current, voltage)
            return web.Response(text="SUCCESS")
        except Exception as e:
            resp = web.Response(text="{}".format(e))
            resp.status = 400
            return resp

    async def disable(self, request):
        channel = int(request.match_info.get("channel"))
        try:
            resp = await self._driver.disable(channel)
            return web.Response(text="SUCCESS")
        except Exception as e:
            resp = web.Response(text="{}".format(e))
            resp.status = 400
            return resp

    async def get_values(self, request):
        channel_info = request.match_info.get("channel_info")
        try:
            channel = None if channel_info == "ALL" else int(channel_info)
            values = await self._driver.get_values(channel)
            return web.json_response(
                values, dumps=partial(json.dumps, default=default_json)
            )
        except Exception as e:
            resp = web.Response(text="{}".format(e))
            resp.status = 400
            return resp

    def start(self):
        with ThreadPoolExecutor() as executor:
            executor.submit(start_log, self._driver)

            loop = asyncio.get_event_loop()
            handler = self.app.make_handler()
            f = loop.create_server(handler, "0.0.0.0", 5555)
            srv = loop.run_until_complete(f)
            loop.run_forever()
