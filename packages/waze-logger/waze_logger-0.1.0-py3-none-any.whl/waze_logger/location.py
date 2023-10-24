""""module for a class containing location"""

from sqlalchemy import Engine, Table, MetaData


class Location:

    location_id: int
    longitude: float
    latitude: float
    name: str

    def __init__(
            self,
            latitude: float,
            longitude: float,
            name: str,
            id: int = None
    ):
        self.longitude = longitude
        self.latitude = latitude
        self.name = name
        self.id = id

    def __str__(self) -> str:
        return f"x:{self.longitude:.14f} y:{self.latitude:.14f}"

    def to_record(self) -> dict:
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "name": self.name,
        }

    @staticmethod
    def from_database(engine: Engine, id: int) -> list["Location"]:

        table = Table("location", MetaData(), autoload_with=engine)
        statement = table.select()

        if id is not None:
            statement = statement.where(table.c.id == id)

        with engine.connect() as connection:

            response = connection.execute(statement)

            headers = response.keys()
            locations = []

            for row in response.fetchall():

                record = dict(zip(headers, row))
                locations.append(Location(**record))

        if id is not None:
            return locations[0]

        return locations
