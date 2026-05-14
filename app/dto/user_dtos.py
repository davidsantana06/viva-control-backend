from flask_restx.fields import Integer, String
from typing import NotRequired, TypedDict

from app.extensions import api
from app.types import UserRole

from .mixin.lifecycle_mixin import lifecycle_mixin


class UserDto(TypedDict):
    id: int
    parent_id: NotRequired[int]
    name: str
    email: str
    role: UserRole


class CreateUserDto(TypedDict):
    parent_id: NotRequired[int]
    name: str
    email: str
    password: str
    role: UserRole


class UpdateUserDto(TypedDict):
    name: str
    email: str
    password: NotRequired[str]


user = api.model(
    "User",
    UserDto(
        id=Integer(readonly=True),
        parent_id=Integer(),
        name=String(),
        email=String(),
        role=String(enum=list(UserRole)),
        **lifecycle_mixin,
    ),
)

create_user = api.model(
    "CreateUser",
    CreateUserDto(
        parent_id=Integer(),
        name=String(required=True, min_length=2, max_length=50),
        email=String(required=True, min_length=5, max_length=255),
        password=String(required=True, min_length=8, max_length=40),
        role=String(required=True, enum=list(UserRole)),
    ),
)

update_user = api.model(
    "UpdateUser",
    UpdateUserDto(
        name=String(min_length=2, max_length=50),
        email=String(min_length=5, max_length=255),
        password=String(min_length=8, max_length=40),
    ),
)
