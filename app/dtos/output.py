from typing import NotRequired, TypedDict

from app.types import UserRole


# auth_

class AccessTokenDto(TypedDict):
    access_token: str


class TokenPairDto(TypedDict):
    access_token: str
    refresh_token: str

# - - -


# customer_

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

# - - -


# distributor_stock_

class DistributorStockDto(TypedDict):
    id: int
    product_id: int
    distributor_id: int
    current_quantity: float
    minimum_quantity: float

# - - -


# payment_method_

class PaymentMethodDto(TypedDict):
    id: int
    name: str

# - - -


# product_

class ProductDto(TypedDict):
    id: int
    name: str
    sku: str
    description: NotRequired[str]
    suggested_price: float

# - - -


# order/order_item_

class OrderItemDto(TypedDict):
    id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: float
    total_price: float


class OrderDto(TypedDict):
    id: int
    customer_id: int
    distributor_id: int
    seller_id: NotRequired[int]
    payment_method_id: NotRequired[int]
    total_amount: float
    discount_pct: int
    discount_amount: float
    net_amount: float
    payment_installments: int
    payment_due_date: str
    notes: NotRequired[str]
    status: str
    is_pending: bool
    is_delivered_unpaid: bool
    is_delivered_paid: bool
    is_cancelled: bool
    items: list[OrderItemDto]

# - - -


# user_

class UserDto(TypedDict):
    id: int
    distributor_id: NotRequired[int]
    name: str
    email: str
    role: UserRole
    is_active: bool

# - - -
