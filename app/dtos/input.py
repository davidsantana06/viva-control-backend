from flask_restx.fields import Integer, String
from typing import NotRequired, TypedDict

from app.extensions import api
from app.types import UserRole


class LoginDto(TypedDict):
    email: str
    password: str


login_dto = api.model(
    "LoginDto",
    LoginDto(
        email=String(required=True, min_length=5, max_length=255),
        password=String(required=True, min_length=8, max_length=40),
    ),
)


class CreateUserDto(TypedDict):
    parent_id: NotRequired[int]
    name: str
    email: str
    password: NotRequired[str]
    password_hash: NotRequired[str]
    role: UserRole


create_user_dto = api.model(
    "CreateUserDto",
    CreateUserDto(
        parent_id=Integer(),
        name=String(required=True, min_length=2, max_length=50),
        email=String(required=True, min_length=5, max_length=255),
        password=String(required=True, min_length=8, max_length=40),
        role=String(required=True, enum=list(UserRole)),
    ),
)


class UpdateUserDto(TypedDict):
    name: str
    email: str
    password: NotRequired[str]
    password_hash: NotRequired[str]


update_user_dto = api.model(
    "UpdateUser",
    UpdateUserDto(
        name=String(min_length=2, max_length=50),
        email=String(min_length=5, max_length=255),
        password=String(min_length=8, max_length=40),
    ),
)
