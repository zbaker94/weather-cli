"""This module provides the weather cli conguration functionality."""
# weather/config.py

from pathlib import Path

import typer

from weather import (
    DIR_ERROR,
    FILE_ERROR,
    SUCCESS,
    __appname__
)

CONFIG_DIR_PATH = Path(typer.get_app_dir(__appname__))
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini"

def init_app(api_key: str) -> int:
    """initialize the application."""
    config_code = _init_config_file()
    if config_code != SUCCESS:
        return config_code
    
    write_code = write_api_key(api_key)
    if write_code != SUCCESS:
        return write_code
    return SUCCESS

def _init_config_file() -> int:
    try:
        print(f"Creating directory: {CONFIG_DIR_PATH}")
        CONFIG_DIR_PATH.mkdir(exist_ok=True)
    except OSError:
        return DIR_ERROR
    try:
        print(f"Creating file: {CONFIG_FILE_PATH}")
        CONFIG_FILE_PATH.touch(exist_ok=True)
    except OSError:
        return FILE_ERROR
    return SUCCESS

def write_api_key(api_key: str) -> int:
    """Write the api key to the config file."""
    try:
        print(f"Writing api key to file: {CONFIG_FILE_PATH}")
        with open(CONFIG_FILE_PATH, "w") as file:
            file.write(f"API_KEY = {api_key}")
    except OSError:
        return FILE_ERROR
    return SUCCESS

def read_api_key() -> str:
    """Read the api key from the config file."""
    try:
        with open(CONFIG_FILE_PATH, "r") as file:
            for line in file:
                if line.startswith("API_KEY"):
                    return line.split("=")[1].strip()
    except OSError:
        return FILE_ERROR