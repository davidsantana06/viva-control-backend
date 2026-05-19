from dataclasses import dataclass
from app.types import UserRole


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
