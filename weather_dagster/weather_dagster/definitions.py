# pylint: disable=assignment-from-no-return
"""Definitions for the weather ETL pipeline."""
from dagster import Definitions, load_assets_from_modules, ScheduleDefinition, define_asset_job

from weather_dagster import assets  # noqa: TID252
from weather_dagster.assets import MongoDBConnectionResource, PostgresConnctionResource

all_assets = load_assets_from_modules([assets])

resources = {
    "mongodb": MongoDBConnectionResource(
        username="admin",
        password="password",
        host="localhost",
        port=27017,
        database="weather_db"
    ),
    "postgres": PostgresConnctionResource(
        username="admin",
        password="password",
        host="localhost",
        port=5432,
        database="weather_db"
    )
}

# Define a job for all assets
weather_job = define_asset_job("weather_job", selection=all_assets)

# Schedule to run every 30 minutes
weather_schedule = ScheduleDefinition(
    job=weather_job,
    cron_schedule="*/15 * * * *",
    description="Run weather ETL every 15 minutes."
)

defs = Definitions(
    assets=all_assets,
    resources=resources,
    schedules=[weather_schedule],
)
