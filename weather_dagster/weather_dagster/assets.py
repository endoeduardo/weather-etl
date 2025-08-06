"""First dag"""
import requests
import dagster as dg
from dagster import AssetExecutionContext, Definitions
from pymongo import MongoClient

from dotenv import load_dotenv
import os
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

class MongoDBConnectionResource(dg.ConfigurableResource):
    """Resource for MongoDB connection."""
    username: str
    password: str
    database: str
    host: str
    port: int

    def mongodb_connection(self):
        """Creates a MongoDB database connection."""
        client = MongoClient(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            authSource=self.database
        )
        return client[self.database]

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
def insert_into_mongodb(
    context: AssetExecutionContext,
    mongodb: MongoDBConnectionResource,
    query_weather_api: dict
) -> None:
    """Inserts the weather data into MongoDB."""
    weather = query_weather_api

    context.log.info(f"Processing weather data: {weather}")

    db = mongodb.mongodb_connection()
    collection = db["weather_data"]

    result = collection.insert_one(weather)
    context.log.info(f"Inserted document with ID: {result.inserted_id}")
