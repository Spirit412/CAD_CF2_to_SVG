import configparser
import os
from pydantic import BaseSettings

here = os.path.abspath(os.path.dirname(__file__))

config = configparser.ConfigParser()
config.read(os.path.join(here, "settings.ini"))


class Settings(BaseSettings):
    ROOT_DIR: str = os.path.normpath(config['SETTINGS']['ROOT_DIR'])
    CF2_DIR: str = os.path.normpath(config['SETTINGS']['CF2_DIR'])


settings = Settings()
