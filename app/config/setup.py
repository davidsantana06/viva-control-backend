from dotenv import load_dotenv
from flask import Flask

from app.extensions import api, cors, db, migrate
from app.apis import user_ns
from . import environs, paths


def _apply_environs(app: Flask) -> None:
    app.json.sort_keys = environs.JSON_SORT_KEYS
    app.config.from_object(environs)


def setup_environs(app: Flask) -> None:
    load_dotenv(paths.ENV_FILE)
    _apply_environs(app)


def _setup_database(app: Flask) -> None:
    db.init_app(app)
    migrate.init_app(app, db)


def _setup_api(app: Flask) -> None:
    api.init_app(app, title="Viva Control", description="Viva Control REST API")
    api.add_namespace(user_ns)


def _setup_cors(app: Flask) -> None:
    cors.init_app(app, origins=environs.ALLOWED_HOSTS)


def setup_extensions(app: Flask) -> None:
    _setup_database(app)
    _setup_api(app)
    _setup_cors(app)
