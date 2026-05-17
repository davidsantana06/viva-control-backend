from dataclasses import dataclass
from enum import StrEnum
from sqlalchemy import ColumnElement, UnaryExpression
from typing import Literal, TypedDict


# dict_

class DistributorFilter(TypedDict):
    distributor_id: int


class ScopedDistributorFilter(TypedDict):
    distributor_id: int
    seller_id: None


class SellerFilter(TypedDict):
    seller_id: int


UserFilter = DistributorFilter | ScopedDistributorFilter | SellerFilter


class JwtClaims(TypedDict):
    distributor_id: int | None
    name: str
    role: "UserRole"
    is_admin: bool
    is_distributor: bool
    is_seller: bool

# - - -


# literal_

SortOrder = Literal["ASC", "DESC"]

# - - -


# tuple_

ExceptionSpecs = tuple[str, int]

# - - -


# enum_

class DocumentType(StrEnum):
    CPF = "CPF"
    CNPJ = "CNPJ"


class OrderStatus(StrEnum):
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"
    DELIVERED_UNPAID = "DELIVERED_UNPAID"
    DELIVERED_PAID = "DELIVERED_PAID"


class UserRole(StrEnum):
    ADMIN = "ADMIN"
    DISTRIBUTOR = "DISTRIBUTOR"
    SELLER = "SELLER"

# - - -


# dataclass_

@dataclass(frozen=True)
class CurrentUser:
    id: int | None
    distributor_id: int
    name: str
    role: "UserRole"
    is_admin: bool
    is_distributor: bool
    is_seller: bool


@dataclass(frozen=True)
class FindAllParams:
    q: str | None
    order: SortOrder
    sort: str
    page: int
    per_page: int


@dataclass(frozen=True)
class UserScopedFindAllParams(FindAllParams):
    user_scoped: bool = False

# - - -


# sqlalchemy_

Filter = ColumnElement[bool]

Ordering = UnaryExpression[object]

# - - -
