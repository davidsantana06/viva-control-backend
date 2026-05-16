from os import environ
from .paths import Paths


class Environs:
    ADMIN_EMAIL = environ.get("ADMIN_EMAIL", "viva@control.com.br")

    ADMIN_PASSWORD = environ.get("ADMIN_PASSWORD", "SUPER-SECURE-ADMIN-PASSWORD")

    ALLOWED_HOSTS = environ.get("ALLOWED_HOSTS", "*").split(" ")

    JSON_SORT_KEYS = False

    JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY", "SUPER-SECURE-JWT-SECRET-KEY")

    SQLALCHEMY_DATABASE_URI = environ.get(
        "DATABASE_URI",
        f"sqlite:///{Paths.SQLITE_FILE}",
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
