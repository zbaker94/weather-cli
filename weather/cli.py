"""This modue provides the weather cli."""
# weather/cli.py

from pathlib import Path
from typing import Optional

import colorama 
from colorama import Fore

import typer

from weather import ERRORS, __appname__, __version__, config, api, SUCCESS, CONFIG_FILE_ERROR

app = typer.Typer()

def check_config() -> bool:
    """Check if the config file exists."""
    if not Path(config.CONFIG_FILE_PATH).is_file():
        typer.echo(Fore.RED + ERRORS[CONFIG_FILE_ERROR])
        raise typer.Exit(CONFIG_FILE_ERROR)
    
    return SUCCESS

def _version_callback(value: bool):
    if value:
        typer.echo(Fore.GREEN + f"{__appname__} version {__version__}")
        raise typer.Exit()

@app.command()
def init(api_key: str = typer.Option(
    str(None),
    "--api-key",
    "-k",
    prompt="the https://www.visualcrossing.com/ api key associated with your account",
)) -> None:
    """Initialize the application."""
    code = config.init_app(api_key)
    if code != config.SUCCESS:
        typer.echo(Fore.RED + ERRORS[code])
        raise typer.Exit(code)
    typer.echo(Fore.GREEN + "Application initialized successfully.")


    
@app.command()
def next_week() -> None:
    """Get the weather for the next week."""
    check_config()
    code = api.get_next_week()
    if code != config.SUCCESS:
        typer.echo(Fore.RED + ERRORS[code])
    raise typer.Exit(code)

@app.callback()
def main(
    version: Optional[bool] = typer.Option(None, "--version", "-v", help="Show the app version and then exit.", callback=_version_callback, is_eager=True)
) -> None:
    return
