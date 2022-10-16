from abc import abstractmethod
import asyncio
import datetime
import logging

CHANNEL_COUNT = 4
LOG_CALLS_INTERVAL = datetime.timedelta(seconds=2)


logging.basicConfig(
    filename="logs.txt",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)


class DeviceBase:
    async def execute(self, command_text):
        pass


class DriverBase:
    @abstractmethod
    async def start_channel(self, channel, current, voltage):
        pass

    @abstractmethod
    async def disable(self, channel):
        pass

    @abstractmethod
    async def get_values(self, channel=None):
        pass


class DriverIml(DriverBase):
    def __init__(self, device):
        assert isinstance(
            device, DeviceBase
        ), "<device> arg must be a type which is derived from DeviceBase"
        self._device = device

    async def start_log(self):
        self._logger = logging.getLogger("DriverIml")
        while True:
            await asyncio.sleep(delay=LOG_CALLS_INTERVAL.seconds)
            await self._write_values()

    async def _write_values(self):
        values = await self.get_values(channel=None)
        self._logger.info(str(values))

    async def start_channel(self, channel, current, voltage):
        assert (
            isinstance(channel, int) and channel >= 1 and channel <= CHANNEL_COUNT
        ), "Channel must be a value from 1,2,3,4"

        await self._device.execute(":SOURce{}:CURRent {}".format(channel, current))
        await self._device.execute(":SOURce{}:VOLTage {}".format(channel, voltage))
        await self._device.execute(":OUTPut{}:STATe ON".format(channel))

    async def disable(self, channel):
        assert (
            isinstance(channel, int) and channel >= 1 and channel <= CHANNEL_COUNT
        ), "Channel must be a value from 1,2,3,4"

        await self._device.execute(":OUTPut{}:STATe OFF".format(channel))

    async def get_values(self, channel=None):
        assert channel is None or (
            isinstance(channel, int) and channel >= 1 and channel <= CHANNEL_COUNT
        ), "Channel must be a value from 1,2,3,4"
        results = {}
        for channel_num in (
            range(1, CHANNEL_COUNT + 1) if channel is None else [channel]
        ):
            resp = await self._device.execute(":MEASure{}:CURRent?".format(channel_num))
            _, current = resp
            time_v, voltage = await self._device.execute(
                ":MEASure{}:VOLTage?".format(channel_num)
            )
            results[channel_num] = {
                "current": current,
                "time": time_v,
                "voltage": voltage,
            }
        return results
