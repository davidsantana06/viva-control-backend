from os import environ
from . import paths


SQLALCHEMY_DATABASE_URI = environ.get(
    "DATABASE_URI",
    f"sqlite:///{paths.SQLITE_FILE}",
)

SQLALCHEMY_TRACK_MODIFICATIONS = False

ALLOWED_HOSTS = environ.get("ALLOWED_HOSTS", "*").split(" ")

JSON_SORT_KEYS = False
