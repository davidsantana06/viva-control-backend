from datetime import timedelta
from os import environ
from .paths import Paths


class Environs:
    ADMIN_EMAIL = environ.get("ADMIN_EMAIL", "viva@control.com.br")

    ADMIN_PASSWORD = environ.get("ADMIN_PASSWORD", "SUPER_SECURE_ADMIN_PASSWORD")

    ALLOWED_HOSTS = environ.get("ALLOWED_HOSTS", "*").split(" ")

    JSON_SORT_KEYS = False

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(
            environ.get(
                "JWT_ACCESS_TOKEN_EXPIRATION_IN_MINUTES",
                15,
            ),
        )
    )

    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(
            environ.get(
                "JWT_REFRESH_TOKEN_EXPIRATION_IN_DAYS",
                30,
            ),
        )
    )

    JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY", "SUPER_SECURE_JWT_SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = environ.get(
        "DATABASE_URI",
        f"sqlite:///{Paths.SQLITE_FILE}",
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
