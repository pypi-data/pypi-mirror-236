"""module containing utility function for sqlachemy engine"""

from urllib.parse import quote as url_encode

from sqlalchemy import Engine
import sqlalchemy as db


def create_engine_url(
    engine: str,
    username: str,
    password: str,
    host: str,
    port: int = None,
    database: str = None,
    query: dict = None,
    connector: str = None,
) -> str:
    """creates an sql engine url based on the parameter provided"""

    engine_url = engine

    if connector is not None:
        engine_url += f"+{connector}"

    engine_url += f"://{username}:{password}@{host}"

    if port is not None:
        engine_url += f":{port}"

    if database is not None:
        engine_url += f"/{database}"

    if query is not None:
        engine_url += f"?{x_url_encode_form(query)}"

    return engine_url


def create_engine(credentials: dict) -> Engine:
    """creates an engine from the credentials provided. Check
    'create_engine_url' for the keys required in the credential
    dictionary"""

    engine_url = create_engine_url(**credentials)

    return db.create_engine(engine_url)


def x_url_encode_form(query: dict):
    """url encode a dictionary for an url based query"""

    items = []

    for key, value in query.items():
        key = url_encode(key)
        value = url_encode(value)

        items.append(f"{key}={value}")

    return "&".join(items)
