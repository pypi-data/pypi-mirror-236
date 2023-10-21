import asyncio
import logging
from asyncio import Event

from victron_ble.devices import BatteryMonitorData, DeviceData

from ch.sachi.victron_ble.powermonitor_scanner import PowermonitorScanner

logger = logging.getLogger(__name__)


class PowerdataReader:
    result: BatteryMonitorData = None
    result_written: Event = Event()

    def __init__(self, id: str, key: str):
        self.id = id
        self.key = key

    async def read(self) -> BatteryMonitorData:
        keys = {self.id: self.key}
        self.result_written = Event(loop=asyncio.get_running_loop())
        scanner = self.create_scanner(keys)
        logger.debug('Scanner created')
        await scanner.scan()

        await self.result_written.wait()
        await scanner.stop()
        return self.result

    def create_scanner(self, keys) -> PowermonitorScanner:
        return PowermonitorScanner(self.cb, keys)

    def cb(self, device_data: DeviceData):
        if isinstance(device_data, BatteryMonitorData):
            self.result = device_data
            logger.debug('cb called on %s', asyncio.get_running_loop())
            self.result_written.set()
