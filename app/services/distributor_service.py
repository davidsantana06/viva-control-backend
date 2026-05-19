from app.exceptions import UserNotFoundException
from app.extensions import db
from app.models import User
from app.types import FindAllParams, UserFilter, UserRole

from .base import UserService


class DistributorService(UserService):
    @classmethod
    def find_first(
        cls,
        id: int,
        user_filter: UserFilter = {},
        *,
        is_active: bool = True,
    ) -> User | None:
        return User.find_first_by_id_and_role(
            id,
            user_filter,
            role=UserRole.DISTRIBUTOR,
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
        return User.find_all_by_role(params, user_filter, role=UserRole.DISTRIBUTOR)

    @classmethod
    def activate(cls, id: int) -> None:
        user = cls.find_first_or_raise(id, is_active=False)
        cls.__toggle_sellers_activation_staged(user)
        User.toggle_activation(user)

    @classmethod
    def deactivate(cls, id: int) -> None:
        user = cls.find_first_or_raise(id)
        cls.__toggle_sellers_activation_staged(user)
        User.toggle_activation(user)

    @classmethod
    def __toggle_sellers_activation_staged(cls, user: User) -> None:
        for seller in user.sellers:
            User.toggle_activation_staged(seller)
            db.session.add(seller)
