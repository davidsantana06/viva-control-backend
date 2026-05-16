from typing import NotRequired, TypedDict

from app.types import UserRole


# auth_

class AccessTokenDto(TypedDict):
    access_token: str

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


# user_

class UserDto(TypedDict):
    id: int
    distributor_id: NotRequired[int]
    name: str
    email: str
    role: UserRole

# - - -
