from typing import NotRequired, TypedDict

from app.types import UserRole


class AccessTokenDto(TypedDict):
    access_token: str


class UserDto(TypedDict):
    id: int
    parent_id: NotRequired[int]
    name: str
    email: str
    role: UserRole
