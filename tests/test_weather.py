# tests/test_weather.py

from typer.testing import CliRunner

from weather import __appname__, __version__, cli

runner = CliRunner()

def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert result.stdout == f"{__appname__} version {__version__}\n"