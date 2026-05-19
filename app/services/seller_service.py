from app.exceptions import UserNotFoundException
from app.models import User
from app.dtos import FindAllParams
from app.types import UserFilter, UserRole

from .base import UserService


class SellerService(UserService):
    @staticmethod
    def find_first(
        id: int,
        user_filter: UserFilter = {},
        *,
        is_active: bool = True,
    ) -> User | None:
        return User.find_first_by_id_and_role(
            id,
            user_filter,
            role=UserRole.SELLER,
            is_active=is_active,
        )

    @classmethod
    def find_first_or_raise(
        cls,
        id: int,
        user_filter: UserFilter = {},
        *,
        is_active: bool = True,
    ) -> User:
        user = cls.find_first(id, user_filter, is_active=is_active)

        if not user:
            raise UserNotFoundException()

        return user

    @staticmethod
    def find_all(params: FindAllParams, user_filter: UserFilter = {}) -> list[User]:
        return User.find_all_by_role(params, user_filter, role=UserRole.SELLER)

    @classmethod
    def activate(cls, id: int, user_filter: UserFilter = {}) -> None:
        user = cls.find_first_or_raise(id, user_filter, is_active=False)
        User.toggle_activation(user)

    @classmethod
    def deactivate(cls, id: int, user_filter: UserFilter = {}) -> None:
        user = cls.find_first_or_raise(id, user_filter)
        User.toggle_activation(user)
