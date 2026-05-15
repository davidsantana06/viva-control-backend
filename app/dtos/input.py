from typing import NotRequired, TypedDict

from app.types import UserRole


class LoginDto(TypedDict):
    email: str
    password: str


class CreateUserDto(TypedDict):
    parent_id: NotRequired[int]
    name: str
    email: str
    password: NotRequired[str]
    password_hash: NotRequired[str]
    role: UserRole


class UpdateUserDto(TypedDict):
    name: str
    email: str
    password: NotRequired[str]
    password_hash: NotRequired[str]
