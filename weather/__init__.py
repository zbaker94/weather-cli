"""Top level package for weather cli."""
# weather/__init__.py

__appname__ = "weather_cli"
__version__ = "0.1.1"

(
    SUCCESS,
    IP_ERROR,
    API_ERROR,
    DIR_ERROR, 
    FILE_ERROR,
    CONFIG_FILE_ERROR,
    CONFIG_VALUE_ERROR,
    LOCATION_ERROR
) = range(8)

ERRORS = {
    SUCCESS: "Success",
    IP_ERROR: "IP address not found",
    API_ERROR: "API error",
    DIR_ERROR: "Directory not found",
    FILE_ERROR: "File not found",
    LOCATION_ERROR: "Location not found or invalid. ",
    CONFIG_FILE_ERROR: "Config file not found. have you run 'init' command?",
    CONFIG_VALUE_ERROR: "Config file does not have a valid api key. have you run 'init' command?",
}
