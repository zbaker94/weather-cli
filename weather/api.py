import typer

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
        "location": {
            "city": g.city,
            "state": g.state,
            "country": g.country
        },
        "hero": parsed_days[0],
        "description": data["description"],
        "days": parsed_days
    }
    # TODO print the parsed data
    print(parsed_data)
    return SUCCESS
