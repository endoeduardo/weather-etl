"""First dag"""
import requests
import dagster as dg
from dagster import AssetExecutionContext

from dotenv import load_dotenv
import os
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


def get_weather_data() -> dict:
    """Fetches weather data from the OpenWeatherMap API."""
    latitude = -25.44
    longitude = -49.27
    url = "https://api.openweathermap.org/data/2.5/weather"
    response = requests.get(
        url,
        params={"lat": latitude, "lon": longitude, "appid": WEATHER_API_KEY},
        timeout=10
    )

    if response.status_code == 200:
        data = response.json()
        return data
    return {}


@dg.asset
def query_weather_api() -> dict:
    """Fetches weather data from the OpenWeatherMap API."""
    return get_weather_data()


@dg.asset
def process_weather_data(context: AssetExecutionContext, query_weather_api: dict) -> dict:
    """Processes the weather data to extract relevant information."""
    weather = query_weather_api

    context.log.info(f"Processing weather data: {weather}")
    return {
        "temperature": weather.get("main", {}).get("temp"),
        "description": weather.get("weather", [{}])[0].get("description"),
    }
