"""weather_cli entry point script."""
# weather/__main__.py

from weather import cli, __appname__

def main() -> None:
    cli.app(prog_name=__appname__)

if __name__ == "__main__":
    main()
