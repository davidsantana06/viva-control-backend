from flask import g
from app.types import CurrentUser


class ApiUtils:
    @staticmethod
    def bind_current_user(current_user: CurrentUser) -> None:
        g.current_user = current_user

    @staticmethod
    def resolve_current_user() -> CurrentUser:
        return g.current_user
