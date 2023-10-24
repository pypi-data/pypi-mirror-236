import json
import os
from typing import Optional

import click


class Config:
    CONFIG_FILE_BASE_PATH: str = os.path.expanduser("~/.opennu/")
    CONFIG_FILE: str = "config.json"

    def __write_key(self, key: str, value: str):
        os.makedirs(self.CONFIG_FILE_BASE_PATH, exist_ok=True)

        config_json = {}
        if os.path.isfile(self.CONFIG_FILE_BASE_PATH + self.CONFIG_FILE):
            config_json = json.load(open(self.CONFIG_FILE_BASE_PATH + self.CONFIG_FILE, "r"))

        config_json[key] = value

        json.dump(config_json, open(self.CONFIG_FILE_BASE_PATH + self.CONFIG_FILE, "w"), indent=4)

    def __get_key(self, key: str) -> Optional[str]:
        if not os.path.isfile(self.CONFIG_FILE_BASE_PATH + self.CONFIG_FILE):
            click.echo("config file not found. Aborting!")
            exit()
        config_json = json.load(open(self.CONFIG_FILE_BASE_PATH + self.CONFIG_FILE, "r"))
        return config_json[key]

    @classmethod
    def get_auth_key(cls):
        return cls.__get_key(cls, "auth_key")

    @classmethod
    def get_base_url(cls):
        return cls.__get_key(cls, "base_url")

    @classmethod
    def write_auth_key(cls, auth_key: str):
        cls.__write_key(cls, "auth_key", auth_key)

    @classmethod
    def write_base_url(cls, base_url: str):
        cls.__write_key(cls, "base_url", base_url)


__all__ = ["Config"]
