from typing import NotRequired, TypedDict

from app.types import UserRole


class AccessTokenDto(TypedDict):
    access_token: str


class PaymentMethodDto(TypedDict):
    id: int
    name: str


class ProductDto(TypedDict):
    id: int
    name: str
    sku: str
    description: NotRequired[str]
    suggested_price: float


class UserDto(TypedDict):
    id: int
    parent_id: NotRequired[int]
    name: str
    email: str
    role: UserRole
