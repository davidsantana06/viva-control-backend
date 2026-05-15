from flask_restx.fields import Integer, String
from typing import NotRequired, TypedDict

from app.extensions import api
from app.types import UserRole
from .mixin.lifecycle_mixin import lifecycle_mixin


class AccessTokenDto(TypedDict):
    access_token: str


access_token_dto = api.model(
    "AccessTokenDto",
    AccessTokenDto(
        access_token=String(),
    ),
)


class UserDto(TypedDict):
    id: int
    parent_id: NotRequired[int]
    name: str
    email: str
    role: UserRole


user_dto = api.model(
    "UserDto",
    UserDto(
        id=Integer(readonly=True),
        parent_id=Integer(),
        name=String(),
        email=String(),
        role=String(enum=list(UserRole)),
        **lifecycle_mixin,
    ),
)
