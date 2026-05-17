from typing import NotRequired, TypedDict

from app.types import DocumentType, OrderStatus, UserRole


# auth_

class LoginDto(TypedDict):
    email: str
    password: str

# - - -


# customer_

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

# - - -


# distributor_stock_

class CreateDistributorStockDto(TypedDict):
    product_id: int
    distributor_id: NotRequired[int]
    current_quantity: float
    minimum_quantity: NotRequired[float]


class UpdateDistributorStockDto(TypedDict):
    current_quantity: NotRequired[float]
    minimum_quantity: NotRequired[float]

# - - -


# payment_method_

class CreatePaymentMethodDto(TypedDict):
    name: str


class UpdatePaymentMethodDto(TypedDict):
    name: NotRequired[str]

# - - -


# product_

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

# - - -


# order/ordem_item_

class CreateOrderItemDto(TypedDict):
    product_id: int
    quantity: float
    unit_price: NotRequired[float]


class CreateOrderDto(TypedDict):
    customer_id: int
    payment_method_id: NotRequired[int]
    discount_pct: float
    payment_installments: int
    payment_due_date: str
    notes: NotRequired[str]
    items: list


class UpdateOrderStatusDto(TypedDict):
    status: OrderStatus

# - - -


# user _

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

# - - -
