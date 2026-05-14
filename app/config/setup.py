from dotenv import load_dotenv
from flask import Flask

from app.apis import user_ns
from app.container import Container
from app.extensions import api, cors, db, migrate
from . import environs, paths


def apply_environs(app: Flask) -> None:
    load_dotenv(paths.ENV_FILE)
    app.json.sort_keys = environs.JSON_SORT_KEYS
    app.config.from_object(environs)


def _init_db(app: Flask) -> None:
    db.init_app(app)
    with app.app_context():
        db.create_all()


def _init_migrate(app: Flask) -> None:
    migrate.init_app(app, db, directory=paths.MIGRATIONS_DIR)


def _init_api(app: Flask) -> None:
    api.init_app(app, title="Viva Control", description="Viva Control REST API")
    api.add_namespace(user_ns)


def _init_cors(app: Flask) -> None:
    cors.init_app(app, origins=environs.ALLOWED_HOSTS)


def init_extensions(app: Flask) -> None:
    _init_db(app)
    _init_migrate(app)
    _init_api(app)
    _init_cors(app)


def init_container(app: Flask) -> None:
    app.container = Container()
