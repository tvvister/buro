import asyncio
import socket

from driver_core.driver import DeviceBase
import datetime  # because of return eval(data) line


class VirtualDevice(DeviceBase):

    _client_socket = None
    _loop = None

    async def execute(self, command_text):
        if self._client_socket is None:
            host = 'localhost'
            port = 5000
            self._client_socket = socket.socket()
            self._client_socket.connect((host, port))
            self._loop = asyncio.get_event_loop()

        await self._loop.sock_sendall(self._client_socket, command_text.encode())
        data = (await self._loop.sock_recv(self._client_socket, 1024)).decode()
        try:
            return eval(data)
        except Exception as exception:
            print(exception)
            return data
