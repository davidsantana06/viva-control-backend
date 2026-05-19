from dataclasses import dataclass
from app.types import SortOrder, UserRole


@dataclass(frozen=True)
class CurrentUser:
    id: int
    distributor_id: int | None
    name: str
    role: str
    is_admin: bool
    is_distributor: bool
    is_seller: bool

    def has_any_role(self, *roles: UserRole) -> bool:
        return self.role in roles


@dataclass(frozen=True)
class FindAllParams:
    q: str | None
    order: SortOrder
    sort: str
    page: int
    per_page: int

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page


@dataclass(frozen=True)
class UserScopedFindAllParams(FindAllParams):
    user_scoped: bool = False
