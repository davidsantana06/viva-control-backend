from flask_restx.fields import String
from typing import TypedDict

from app.extensions import api


class LoginDto(TypedDict):
    email: str
    password: str


class AccessTokenDto(TypedDict):
    access_token: str


login_dto = api.model(
    "Login",
    LoginDto(
        email=String(required=True, min_length=5, max_length=255),
        password=String(required=True, min_length=8, max_length=40),
    ),
)

access_token_dto = api.model(
    "Token",
    AccessTokenDto(
        access_token=String(),
    ),
)
