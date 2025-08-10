from dagster import Definitions, load_assets_from_modules

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

defs = Definitions(
    assets=all_assets,
    resources=resources,
)
