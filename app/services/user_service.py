from app.dtos import CreateUserDto, UpdateUserDto
from app.exceptions import (
    AdminDisableNotAllowedException,
    EmailAlreadyRegisteredException,
    UserNotFoundException,
)
from app.extensions import db
from app.models import User
from app.facades import Security
from app.types import FindAllParams, UserFilter


class UserService:
    @staticmethod
    def create(dto: CreateUserDto) -> User:
        other_user = User.find_first_by_email(dto["email"])
        if other_user:
            raise EmailAlreadyRegisteredException()

        dto["password_hash"] = Security.hash_password(dto.pop("password"))
        user = User(**dto)
        User.save(user)
        return user

    @staticmethod
    def find_all(params: FindAllParams, user_filter: UserFilter) -> list[User]:
        return User.find_all(params, user_filter)

    @staticmethod
    def find_first(id: int, user_filter: UserFilter) -> User | None:
        return User.find_first_by_id(id, user_filter)

    @classmethod
    def find_first_or_raise(cls, id: int, user_filter: UserFilter) -> User:
        user = cls.find_first(id, user_filter)

        if not user:
            raise UserNotFoundException()

        return user

    @classmethod
    def update(cls, id: int, dto: UpdateUserDto, user_filter: UserFilter) -> User:
        user = cls.find_first_or_raise(id, user_filter)
        if dto.get("password"):
            dto["password_hash"] = Security.hash_password(dto.pop("password"))
        user.update(**dto)
        User.save(user)
        return user

    @classmethod
    def disable(cls, id: int) -> None:
        user = User.find_first_by_id(id, is_active=True)

        if not user:
            raise UserNotFoundException()

        if user.is_admin:
            raise AdminDisableNotAllowedException()

        if user.is_distributor:
            cls.__toggle_sellers_activation_staged(user)

        User.toggle_activation(user)
        db.session.add(user)
        db.session.commit()

    @classmethod
    def activate(cls, id: int) -> None:
        user = User.find_first_by_id(id, is_active=False)

        if not user:
            raise UserNotFoundException()

        if user.is_distributor:
            cls.__toggle_sellers_activation_staged(user)

        User.toggle_activation(user)
        db.session.add(user)
        db.session.commit()

    @classmethod
    def __toggle_sellers_activation_staged(cls, user: User) -> None:
        for seller in user.sellers:
            User.toggle_activation(seller)
            db.session.add(seller)
