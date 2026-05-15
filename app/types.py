from dataclasses import dataclass
from enum import StrEnum
from sqlalchemy import ColumnElement, UnaryExpression
from typing import Literal, NotRequired, TypedDict


# dict_

class RoleFilter(TypedDict):
    distributor_id: NotRequired[int]
    seller_id: NotRequired[int]


class JwtClaims(TypedDict):
    name: str
    role: "UserRole"

# - - -


# literal_

SortOrder = Literal["ASC", "DESC"]

# - - -


# tuple_

ExceptionSpecs = tuple[str, int]

# - - -


# enum_

class UserRole(StrEnum):
    ADMIN = "ADMIN"
    DISTRIBUTOR = "DISTRIBUTOR"
    SELLER = "SELLER"

# - - -


# dataclass

@dataclass(frozen=True)
class CurrentUser:
    id: int
    role: "UserRole"


@dataclass(frozen=True)
class FindAllParams:
    q: str | None
    order: SortOrder
    sort: str
    page: int
    per_page: int

# - - -


# sqlalchemy

Filter = ColumnElement[bool]

Ordering = UnaryExpression[object]

# - - -
