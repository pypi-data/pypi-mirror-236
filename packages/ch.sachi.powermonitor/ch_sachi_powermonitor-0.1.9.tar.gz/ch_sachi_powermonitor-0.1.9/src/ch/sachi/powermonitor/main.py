import asyncio
import logging

import click

from ch.sachi.powermonitor.config import read_config, Config
from ch.sachi.powermonitor.powermonitor_repository import MonitorRepository
from ch.sachi.powermonitor.powerdata_reader import PowerdataReader
from ch.sachi.powermonitor.restService_powerdata import RestServicePowerdata

logger = logging.getLogger(__name__)
log_level = logging.INFO


@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Increase logging output")
def cli(verbose):
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(name)-6s %(message)s', level=log_level)


def create_monitor_repository() -> MonitorRepository:
    repo = MonitorRepository('powermon.db')
    repo.init()
    return repo


@cli.command(help="Read data from configured Batterymonitor")
@click.option('-c', '--configuration', default='powermonitor.cfg', help="Configuration file")
def read(configuration):
    logger.warning('Logfile: %s', configuration)
    config = read_config(configuration)

    data_reader = PowerdataReader(config.victron_ble.id, config.victron_ble.key)

    async def doit():
        logger.info("Reading")
        result = await asyncio.wait_for(data_reader.read(), 20)
        repo = create_monitor_repository()
        if result is not None:
            repo.write(result)

    asyncio.run(doit())


@cli.command(help="Publish data to configured rest endpoint")
@click.option('-c', '--configuration', default='powermonitor.cfg', help="Configuration file")
def publish(configuration):
    config = read_config(configuration)
    repo = create_monitor_repository()
    service = RestServicePowerdata(config.rest.url, config.rest.username, config.rest.password)
    last = service.get_last_timestamp()
    measures_to_post = repo.get_measures_after(last)
    if len(measures_to_post) > 0:
        logger.info('Posting ' + str(measures_to_post) + "'")
        service.post_measures(measures_to_post)


if __name__ == '__main__':
    cli()
if __name__ == '__publish__':
    publish()
