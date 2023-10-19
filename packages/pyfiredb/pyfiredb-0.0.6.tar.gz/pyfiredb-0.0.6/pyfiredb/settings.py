from dataclasses import dataclass
import json


@dataclass
class Settings:
    with open('config.json') as config_file:
        config = json.load(config_file)

    setup = config['DB_SETUP']


@dataclass
class Credentials:
    with open('config.json') as config_file:
        config = json.load(config_file)

    user = config['DB_USER']
    password = config['DB_PASS']
