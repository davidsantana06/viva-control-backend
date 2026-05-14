from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended.exceptions import InvalidHeaderError, JWTExtendedException
from http import HTTPStatus
from jwt.exceptions import PyJWTError

from app.apis import auth_ns, user_ns
from app.extensions import api, cors, db, jwt, migrate
from . import environs, paths


_API_AUTHORIZATIONS = {
    "Bearer": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Bearer <token>",
    }
}


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


def _init_jwt(app: Flask) -> None:
    jwt.init_app(app)


def _init_api(app: Flask) -> None:
    api.init_app(
        app,
        title="Viva Control Backend",
        description="Viva Control REST API",
    )

    api.add_namespace(auth_ns)
    api.add_namespace(user_ns)

    api.authorizations = _API_AUTHORIZATIONS

    api.errorhandler(
        InvalidHeaderError,
        lambda _: ({"message": "Invalid authorization header"}, HTTPStatus.UNPROCESSABLE_CONTENT),
    )
    api.errorhandler(
        JWTExtendedException,
        lambda _: ({"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED),
    )
    api.errorhandler(
        PyJWTError,
        lambda _: ({"message": "Invalid token"}, HTTPStatus.UNPROCESSABLE_CONTENT),
    )


def _init_cors(app: Flask) -> None:
    cors.init_app(app, origins=environs.ALLOWED_HOSTS)


def init_extensions(app: Flask) -> None:
    _init_db(app)
    _init_migrate(app)
    _init_jwt(app)
    _init_api(app)
    _init_cors(app)
