from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended.exceptions import InvalidHeaderError, JWTExtendedException
from http import HTTPStatus
from jwt.exceptions import PyJWTError

from app.apis import auth_ns, user_ns
from app.extensions import api, cors, db, jwt, migrate

from .environs import Environs
from .paths import Paths


class Setup:
    __API_AUTHORIZATIONS = {
        "Bearer": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Bearer <token>",
        }
    }

    @staticmethod
    def apply_environs(app: Flask) -> None:
        load_dotenv(Paths.ENV_FILE)
        app.json.sort_keys = Environs.JSON_SORT_KEYS
        app.config.from_object(Environs)

    @staticmethod
    def __init_db(app: Flask) -> None:
        db.init_app(app)
        with app.app_context():
            db.create_all()

    @staticmethod
    def __init_migrate(app: Flask) -> None:
        migrate.init_app(app, db, directory=Paths.MIGRATIONS_DIR)

    @staticmethod
    def __init_jwt(app: Flask) -> None:
        jwt.init_app(app)

    @classmethod
    def __init_api(cls, app: Flask) -> None:
        api.init_app(
            app,
            title="Viva Control Backend",
            description="Viva Control REST API",
        )

        api.add_namespace(auth_ns)
        api.add_namespace(user_ns)

        api.authorizations = cls.__API_AUTHORIZATIONS

        api.errorhandler(
            InvalidHeaderError,
            lambda _: (
                {"message": "Invalid authorization header"},
                HTTPStatus.UNPROCESSABLE_CONTENT,
            ),
        )
        api.errorhandler(
            JWTExtendedException,
            lambda _: (
                {"message": "Unauthorized"},
                HTTPStatus.UNAUTHORIZED,
            ),
        )
        api.errorhandler(
            PyJWTError,
            lambda _: (
                {"message": "Invalid token"},
                HTTPStatus.UNPROCESSABLE_CONTENT,
            ),
        )

    @staticmethod
    def __init_cors(app: Flask) -> None:
        cors.init_app(app, origins=Environs.ALLOWED_HOSTS)

    @classmethod
    def init_extensions(cls, app: Flask) -> None:
        cls.__init_db(app)
        cls.__init_migrate(app)
        cls.__init_jwt(app)
        cls.__init_api(app)
        cls.__init_cors(app)
