from enum import StrEnum
from typing import Literal


SortOrder = Literal["ASC", "DESC"]


class UserRole(StrEnum):
    DISTRIBUTOR = "DISTRIBUTOR"
    SELLER = "SELLER"
