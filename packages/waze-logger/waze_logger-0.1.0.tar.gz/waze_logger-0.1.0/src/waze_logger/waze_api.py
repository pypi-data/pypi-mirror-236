"""utility function for interacting with waze api"""

import json
import datetime as dt

import requests

from waze_logger.location import Location


WAZE_URL = "https://waze.com"
ROUTING_ENDPOINT = "RoutingManager/routingRequest"

DEFAULT_HEADERS = {
    "User-Agent": "PostmanRuntime/7.33.0"
}


def get_route(origin: Location, destination: Location) -> dict:

    params = {
        "from": str(origin),
        "to": str(destination),
        "returnJSON": "true",
        "at": 0,
        "nPaths": 1,
    }

    url = f"{WAZE_URL}/{ROUTING_ENDPOINT}"

    response = requests.get(url=url, params=params, headers=DEFAULT_HEADERS)

    return json.loads(response.text)["response"]


def get_route_duration(
    origin: Location,
    destination: Location,
) -> int:

    route = get_route(origin, destination)

    return route["totalRouteTime"]


if __name__ == '__main__':

    ORIGIN = Location(45.760919431034004, -73.98788574519124)
    DESTINATION = Location(45.47939592085909, -73.805993034125)

    location_str = str(ORIGIN)

    route = get_route_duration(ORIGIN, DESTINATION)

    foo = "bar"
