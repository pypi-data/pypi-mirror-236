"""module used for the creation of the database on setup"""

from itertools import combinations

import sqlalchemy as db

from waze_logger.location import Location
from waze_logger.route import Route


def create_database(
        engine: db.Engine,
        locations: list[Location] = None,
        force: bool = False,
):

    # check if tables exist and if so drop before continuing
    metadata = db.MetaData()
    metadata.reflect(engine)

    if len(metadata.tables.keys()) > 0 and not force:
        raise ValueError(
            "The database contains tables. Aborting. To clear the database,"
            "set 'force' to true"
        )
    elif len(metadata.tables.keys()) > 0 and force:
        metadata.drop_all(bind=engine)

    _create_table(engine)

    if locations is not None:

        # create the locations in the database and retrieve them with
        # ids
        locations = _create_locations(engine, locations)

        # get all pairs of locations
        possible_routes = combinations(locations, 2)
        routes = []

        for route in possible_routes:
            routes.append(Route(route[0], route[1]))
            routes.append(Route(route[1], route[0]))

        routes = _create_routes(engine, routes)


def _create_routes(
        engine: db.Engine,
        routes: list[Route],
) -> list[Route]:

    meta_data = db.MetaData()

    table = db.Table("route", meta_data, autoload_with=engine)

    with engine.connect() as connection:

        # insert the routes
        records = [x.to_record() for x in routes]
        connection.execute(db.insert(table), records)
        connection.commit()

        response = connection.execute(db.select(table))


def _create_locations(
        engine: db.Engine,
        locations: list[Location]
) -> list[Location]:

    meta_data = db.MetaData()

    table = db.Table("location", meta_data, autoload_with=engine)

    with engine.connect() as connection:

        # insert the locations
        records = [x.to_record() for x in locations]
        connection.execute(db.insert(table), records)
        connection.commit()

        # retrieve the records with id from the database
        response = connection.execute(db.select(table))
        headers = response.keys()

        locations = []
        for row in response.fetchall():
            locations.append(dict(zip(headers, row)))

        return [Location(**x) for x in locations]


def _create_table(engine: db.Engine):

    meta_data = db.MetaData()

    db.Table(
        "location", meta_data,
        db.Column("id", db.Integer, primary_key=True, autoincrement=True),
        db.Column("name", db.String(32), nullable=False),
        db.Column("latitude", db.DECIMAL(8, 5), nullable=False),
        db.Column("longitude", db.DECIMAL(7, 5), nullable=False),
        db.UniqueConstraint("latitude", "longitude", name="unique_location"),
        db.CheckConstraint(
            "latitude >= -180 AND latitude <= 180",
            name="latitude_scope"
        ),
        db.CheckConstraint(
            "longitude >= -90 AND longitude <= 90",
            name="longitude_scope"
        ),
    )

    db.Table(
        "route", meta_data,
        db.Column("id", db.Integer, primary_key=True, autoincrement=True),
        db.Column("origin", db.ForeignKey("location.id"), nullable=False),
        db.Column("destination", db.ForeignKey("location.id"), nullable=False),
        db.UniqueConstraint("origin", "destination", name="unique_route")
    )

    db.Table(
        "route_duration", meta_data,
        db.Column("logged_time", db.DateTime),
        db.Column("route", db.ForeignKey("route.id")),
        db.Column("trip_duration", db.Integer),
        db.PrimaryKeyConstraint("logged_time", "route",
                                name="route_duration_pk"),
    )

    meta_data.create_all(engine)
