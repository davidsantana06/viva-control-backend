from typing import NotRequired, TypedDict

from app.types import UserRole


class AccessTokenDto(TypedDict):
    access_token: str


class CustomerDto(TypedDict):
    id: int
    distributor_id: int
    seller_id: NotRequired[int]
    name: str
    document: str
    document_type: str
    phone: NotRequired[str]
    address: NotRequired[str]
    birth_date: NotRequired[str]
    notes: NotRequired[str]


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
    distributor_id: NotRequired[int]
    name: str
    email: str
    role: UserRole
