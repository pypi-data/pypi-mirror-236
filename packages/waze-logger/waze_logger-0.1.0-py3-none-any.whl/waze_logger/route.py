"""module containing the route object"""

import datetime as dt

from sqlalchemy import Engine, Table, MetaData

from waze_logger.location import Location
from waze_logger.waze_api import get_route_duration


class Route:

    id: int
    origin: Location
    destination: Location

    def __init__(
            self,
            origin: Location,
            destination: Location,
            id: int = None,
    ):

        self.origin = origin
        self.destination = destination
        self.id = id

    def to_record(self) -> dict:
        return {
            "origin": self.origin.id,
            "destination": self.destination.id,
        }

    def duration(self) -> int:
        return get_route_duration(self.origin, self.destination)

    @staticmethod
    def from_database(engine: Engine, id: int = None) -> list["Route"]:

        table = Table("route", MetaData(), autoload_with=engine)
        statement = table.select()

        if id is not None:
            statement = statement.where(table.c.id == id)

        with engine.connect() as connection:

            response = connection.execute(statement)

            headers = response.keys()
            routes = []

            for row in response.fetchall():

                record = dict(zip(headers, row))

                # convert location id into location objects
                record["origin"] = Location.from_database(
                    engine,
                    record["origin"]
                )

                record["destination"] = Location.from_database(
                    engine,
                    record["destination"]
                )

                routes.append(Route(**record))

        if id is not None:
            return routes[0]

        return routes
