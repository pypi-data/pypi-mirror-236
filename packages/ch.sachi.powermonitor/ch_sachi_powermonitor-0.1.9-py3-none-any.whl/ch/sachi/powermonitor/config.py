import configparser
import string


class RestConfig:
    def __init__(self, url: str, username: str, password: str):
        self.url = url
        self.username = username
        self.password = password


class VictronBleConfig:
    def __init__(self, id: str, key: str, ):
        if id is None or key is None:
            raise ValueError('We need id and key')
        self.id = id
        self.key = key


class Config:
    def __init__(self, victron_ble: VictronBleConfig, rest: RestConfig):
        self.rest = rest
        self.victron_ble = victron_ble


def read_config(config_file: string) -> Config:
    config = configparser.ConfigParser()
    config.read(config_file)
    if not config.has_section('victron_ble'):
        raise ValueError('no section victron_ble')
    if not config.has_section('rest'):
        raise ValueError('no section rest')
    victron_ble = config['victron_ble']
    victron_conf = VictronBleConfig(victron_ble.get('id'), victron_ble.get('key'))
    rest = config['rest']
    rest_conf = RestConfig(rest.get('url'), rest.get('username'), rest.get('password'))
    return Config(victron_conf, rest_conf)
