from abc import ABC, abstractmethod

from app.dtos import CreateUserDto, UpdateUserDto
from app.exceptions import EmailAlreadyRegisteredException
from app.facades import Security
from app.models import User
from app.types import FindAllParams, UserFilter


class UserService(ABC):
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
    @abstractmethod
    def find_first(
        id: int,
        user_filter: UserFilter,
        *,
        is_active: bool = True,
    ) -> User | None: ...

    @classmethod
    @abstractmethod
    def find_first_or_raise(
        cls,
        id: int,
        user_filter: UserFilter,
        *,
        is_active: bool = True,
    ) -> User: ...

    @staticmethod
    @abstractmethod
    def find_all(params: FindAllParams, user_filter: UserFilter) -> list[User]: ...

    @classmethod
    def update(cls, id: int, dto: UpdateUserDto, user_filter: UserFilter = {}) -> User:
        user = cls.find_first_or_raise(id, user_filter)
        if dto.get("password"):
            dto["password_hash"] = Security.hash_password(dto.pop("password"))
        user.update(**dto)
        User.save(user)
        return user

    @classmethod
    @abstractmethod
    def activate(cls, id: int) -> None: ...

    @classmethod
    @abstractmethod
    def deactivate(cls, id: int) -> None: ...
