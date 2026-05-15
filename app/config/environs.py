from os import environ
from .paths import Paths


class Environs:
    SQLALCHEMY_DATABASE_URI = environ.get(
        "DATABASE_URI",
        f"sqlite:///{Paths.SQLITE_FILE}",
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ALLOWED_HOSTS = environ.get("ALLOWED_HOSTS", "*").split(" ")

    JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY", "VIVA_CONTROL__by__davidsantana06")

    JSON_SORT_KEYS = False
