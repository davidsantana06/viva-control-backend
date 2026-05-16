from typing import NotRequired, TypedDict

from app.types import DocumentType, UserRole


class LoginDto(TypedDict):
    email: str
    password: str


class CreateCustomerDto(TypedDict):
    distributor_id: NotRequired[int]
    seller_id: NotRequired[int]
    name: str
    document: str
    document_type: DocumentType
    phone: NotRequired[str]
    address: NotRequired[str]
    birth_date: NotRequired[str]
    notes: NotRequired[str]


class UpdateCustomerDto(TypedDict):
    name: NotRequired[str]
    phone: NotRequired[str]
    address: NotRequired[str]
    birth_date: NotRequired[str]
    notes: NotRequired[str]


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
    distributor_id: NotRequired[int]
    name: str
    email: str
    password: NotRequired[str]
    password_hash: NotRequired[str]
    role: UserRole


class UpdateUserDto(TypedDict):
    name: NotRequired[str]
    email: NotRequired[str]
    password: NotRequired[str]
    password_hash: NotRequired[str]
