"""Top level package for weather cli."""
# weather/__init__.py

__appname__ = "weather_cli"
__version__ = "0.1.1"

(
    SUCCESS,
    IP_ERROR,
    API_ERROR,
) = range(3)

ERRORS = {
    SUCCESS: "Success",
    IP_ERROR: "IP address not found",
    API_ERROR: "API error",
}
