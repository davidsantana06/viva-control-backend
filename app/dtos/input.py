from typing import NotRequired, TypedDict

from app.types import UserRole


class LoginDto(TypedDict):
    email: str
    password: str


class CreatePaymentMethodDto(TypedDict):
    name: str


class UpdatePaymentMethodDto(TypedDict):
    name: NotRequired[str]


class CreateProductDto(TypedDict):
    name: str
    sku: str
    description: NotRequired[str]
    suggested_price: float


class UpdateProductDto(TypedDict):
    name: NotRequired[str]
    sku: NotRequired[str]
    description: NotRequired[str]
    suggested_price: NotRequired[float]


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
