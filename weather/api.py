import typer

import os

columns, lines = os.get_terminal_size()


import geocoder
from geocoder import ip

import requests
import json

import datetime

from weather.config import read_api_key

from weather import LOCATION_ERROR, API_ERROR, SUCCESS

api_key = read_api_key()


def _get_user_location() -> geocoder.ipinfo:
    """Get the location of the user."""
    try:
        g = geocoder.ip('me')
        return g
    except Exception as e:
        typer.echo(f"Error: {e}")
        return None

def _parse_day(day: dict) -> dict:
    """parse a single day of weather data."""
    date = day["datetime"]
    epoch = day["datetimeEpoch"]
    max_temp = day["tempmax"]
    min_temp = day["tempmin"]
    temp = day["temp"]
    feels_like_max = day["feelslikemax"]
    feels_like_min = day["feelslikemin"]
    feels_like = day["feelslike"]
    humidity = day["humidity"]
    rain_chance = day["precipprob"] if "preciptype" in day and day["preciptype"] != None and "rain" in day["preciptype"] else 0
    conditions = day["conditions"]
    description = day["description"]
    icon = day["icon"]

    return {
        "date": date,
        "epoch": epoch,
        "max_temp": max_temp,
        "min_temp": min_temp,
        "temp": temp,
        "feels_like_max": feels_like_max,
        "feels_like_min": feels_like_min,
        "feels_like": feels_like,
        "humidity": humidity,
        "rain_chance": rain_chance,
        "conditions": conditions,
        "description": description,
        "icon": icon
    }
    

def _parse_days(days: list) -> list:
    """Parse a list containing days of weather data."""
    return [_parse_day(day) for day in days]

def _print_header(data: dict):
    """Print the header of the weather data."""
    location_text = f"Weather for {data['location']['city']}, {data['location']['state']}, {data['location']['country']}"
    description_text = f"{data['description']}"
    start_date = data['dates']["start"]
    end_date = data['dates']["end"]
    date_text = start_date

    if (end_date != None and end_date != start_date):
        date_text += f" - {end_date}"

    # header_width = max(len(location_text), len(description_text)) + 14

    location_text = "#" + location_text.center(columns -2, " ") + "#"
    description_text = "#" + description_text.center(columns -2, " ") + "#"
    date_text = "#" + date_text.center(columns -2, " ") + "#"
    typer.echo("#" * columns)
    typer.echo(location_text)
    typer.echo(date_text)
    typer.echo(description_text)
    typer.echo("#" * columns)

def _print_day(day: dict, span: int = 33):
    """print a given day of weather data. spanning the given percentage of the terminal width."""
    column_span = int(span * columns / 100)
    header = f" {day['date']} - {day['conditions']} "
    header = header.center(column_span, "#")
    typer.echo(header)

    temperature_info = "#" + f" Current: {day['temp']}F, High: {day['max_temp']}F, Low: {day['min_temp']}F".center(column_span -3, " ") + "#"
    typer.echo(temperature_info)

    feels_like_info = "#" + f" Feels like: {day['feels_like']}F, High: {day['feels_like_max']}F, Low: {day['feels_like_min']}F".center(column_span -3, " ") + "#"
    typer.echo(feels_like_info)

    humidity_info = "#" + f" Humidity: {day['humidity']}%, Rain Chance: {day['rain_chance']}%".center(column_span -3, " ") + "#"
    typer.echo(humidity_info)

    typer.echo("#" * column_span)

def _print_days(days: list):
    """Print all the days of weather data."""
    for day in days:
        _print_day(day, 100)

def get_next_week():
    """Get the weather for the next week."""
    g = _get_user_location()
    if g is None:
        return LOCATION_ERROR
    
    lat = g.latlng[0]
    lon = g.latlng[1]
    date_time = datetime.datetime.now()
    start_date = date_time.strftime("%Y-%m-%d")
    end_date = (date_time + datetime.timedelta(days=7)).strftime("%Y-%m-%d")

    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{lat},{lon}/{start_date}/{end_date}?unitGroup=us&key={api_key}&contentType=json"

    response = requests.get(url)
    if response.status_code != 200:
        return API_ERROR
    
    data = json.loads(response.text)
    parsed_days = _parse_days(data["days"])
    parsed_data = {
        "dates": {
            "start": start_date,
            "end": end_date
        },
        "location": {
            "city": g.city,
            "state": g.state,
            "country": g.country
        },
        "hero": parsed_days[0],
        "description": data["description"],
        "days": parsed_days
    }
    _print_header(parsed_data)
    _print_days(parsed_days)
    return SUCCESS
