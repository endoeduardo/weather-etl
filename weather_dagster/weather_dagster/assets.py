"""First dag"""
import os
from datetime import datetime, timedelta

import requests
import dagster as dg
from dagster import AssetExecutionContext
from pymongo import MongoClient
from psycopg2 import connect, sql

from dotenv import load_dotenv
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


class PostgresConnctionResource(dg.ConfigurableResource):
    """Resource for PostgreSQL db connection"""
    username: str
    password: str
    database: str
    host: str
    port: int

    def postgres_connection(self):
        """Creates a PostgreSQL db connection"""
        conn = connect(
            dbname=self.database,
            user=self.username,
            password=self.password,
            host=self.host,
            port=self.port
        )
        return conn


def get_weather_data(latitude: float, longitude: float) -> dict:
    """Fetches weather data from the OpenWeatherMap API."""
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
def fetch_weather_data(
    context: AssetExecutionContext,
    postgres: PostgresConnctionResource,
    mongodb: MongoDBConnectionResource,
) -> str:
    """Inserts the weather data into MongoDB."""

    # Establish connection with dbs
    db = mongodb.mongodb_connection()
    conn = postgres.postgres_connection()

    # Fetch locations to be processed
    cursor = conn.cursor()
    cursor.execute(
        """
            SELECT id, latitude, longitude, city, state FROM locations
        """
    )
    locations = cursor.fetchall()

    for location in locations:
        latitude = location[1]
        longitude = location[2]
        city = location[3]
        state = location[4]

        # Queries the API and saves the result in MongoDB
        context.log.info(f"Processing weather data: {city} - {state}")
        weather = get_weather_data(latitude, longitude)

        if not weather:
            context.log.warning(f"No weather data found for: {city} - {state}")
            continue

        collection = db["weather_data"]

        weather["location_id"] = location[0]
        result = collection.insert_one(weather)
        context.log.info(f"Inserted document with ID: {result.inserted_id}")

    cursor.close()
    conn.close()

    return "done"

@dg.asset
def insert_into_postgres(
    context: AssetExecutionContext,
    mongodb: MongoDBConnectionResource,
    postgres: PostgresConnctionResource,
    fetch_weather_data: str,  # Ensure this asset runs after fetch_weather_data
) -> None:
    """Inserts the weather data into PostgreSQL."""
    context.log.info("Reading from Mongo and inserting in Postgres")
    data = mongodb.mongodb_connection()["weather_data"].find(
        {"dt": {"$gte": (datetime.now() - timedelta(minutes=15)).timestamp()}},
        sort=[("dt", -1)]
    )
    if not data:
        context.log.warning("No new weather data found.")
        return

    conn = postgres.postgres_connection()
    cursor = conn.cursor()
    try:
        for weather in data:
            cursor.execute(
                sql.SQL("""
                    INSERT INTO forecast (location_id, forecast_date, temperature, temperature_min, temperature_max, feels_like, condition)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """),
                (
                    weather["location_id"],
                    datetime.fromtimestamp(weather["dt"]),
                    weather["main"]["temp"],
                    weather["main"]["temp_min"],
                    weather["main"]["temp_max"],
                    weather["main"]["feels_like"],
                    weather["weather"][0]["description"]
                )
            )
        conn.commit()
        context.log.info("Inserted data into PostgreSQL successfully.")
    except Exception as e:
        context.log.error(f"Error inserting data into PostgreSQL: {e}")
    finally:
        cursor.close()
        conn.close()
