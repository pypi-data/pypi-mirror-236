"""main module containing the cli"""

import argparse
import logging
import json
import csv
import datetime as dt
from time import sleep
from pathlib import Path

from sqlalchemy import Engine, Table, MetaData

from waze_logger.database.engine import create_engine
from waze_logger.database.create import create_database
from waze_logger.location import Location
from waze_logger.route import Route

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def get_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        "waze_logger",
        description=(
            "A utility to log waze route time from their API into a database"
        ),
    )

    parser.add_argument(
        "-c", "--config-file",
        help=(
            "location of the configuration file containing the credentials for"
            " the database"
        ),
        default=Path.home() / ".config/waze_logger/config.json",
        type=Path,
    )

    parser.add_argument(
        "-s", "--setup",
        help="creates the setup make to create the database.",
        default=False,
    )

    parser.add_argument(
        "-f", "--force",
        help="forces the setup of the database even if it contains data",
        default=False,
    )

    parser.add_argument(
        "--locations",
        help="path to a csv file containing location to include in the setup",
        default=None,
        type=Path,
    )

    return parser.parse_args()


def main():

    args = get_args()

    LOGGER.info("Reading the configuration file")

    with open(args.config_file, 'r', encoding="utf8") as file:
        config = json.load(file)

    engine = create_engine(config["database"])

    if args.setup:
        LOGGER.info("Setting the database")
        locations = _prep_location(args.locations)
        create_database(engine, locations, args.force)
        return None

    # get the list of routes from the database
    routes = Route.from_database(engine)

    log_routes(routes, engine)


def log_routes(routes: list[Route], engine: Engine):

    if len(routes) == 0:
        return None

    durations = []

    for route in routes:

        duration = route.duration()

        durations.append({
            "route": route.id,
            "trip_duration": duration,
            "logged_time": dt.datetime.now(),
        })
        LOGGER.info(f"route {route.id} -> {duration}")
        sleep(1)

    with engine.connect() as connection:

        table = Table("route_duration", MetaData(), autoload_with=engine)
        connection.execute(table.insert(), durations)
        connection.commit()


def _prep_location(file_path: str) -> list[Location]:

    if file_path is None:
        return None

    with open(file_path, 'r', encoding="utf8") as file:
        csv_file = csv.reader(file)

        headers = next(csv_file)

        locations = []

        for row in csv_file:

            record = dict(zip(headers, row))
            locations.append(Location(**record))

    return locations


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        LOGGER.info("Aborting process")
