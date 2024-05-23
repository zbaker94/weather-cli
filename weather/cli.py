"""This modue provides the weather cli."""
# weather/cli.py

from typing import Optional

import typer

from weather import __appname__, __version__

app = typer.Typer()

def _version_callback(value: bool):
    if value:
        typer.echo(f"{__appname__} version {__version__}")
        raise typer.Exit()
    
@app.callback()
def main(
    version: Optional[bool] = typer.Option(None, "--version", "-v", help="Show the app version and then exit.", callback=_version_callback, is_eager=True)
) -> None:
    return
