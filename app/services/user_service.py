from app.dtos import CreateUserDto, UpdateUserDto
from app.exceptions import AdminDeactivationNotAllowed, EmailAlreadyInUse, UserNotFound
from app.models import User
from app.proxies import HashProxy
from app.types import FindAllParams


class UserService:
    @staticmethod
    def create(dto: CreateUserDto) -> User:
        other_user = User.find_first_by_email(dto["email"])
        if other_user:
            raise EmailAlreadyInUse()

        dto["password_hash"] = HashProxy.hash(dto.pop("password"))
        user = User(**dto)
        User.save(user)
        return user

    @staticmethod
    def find_all(params: FindAllParams) -> list[User]:
        return User.find_all(params)

    @staticmethod
    def find_first(id: int) -> User:
        user = User.find_first_by_id(id)

        if not user:
            raise UserNotFound()

        return user

    @classmethod
    def update(cls, id: int, dto: UpdateUserDto) -> User:
        user = cls.find_first(id)

        if dto.get("password"):
            dto["password_hash"] = HashProxy.hash(dto.pop("password"))

        user.update(**dto)
        User.save(user)
        return user

    @classmethod
    def deactivate(cls, id: int) -> None:
        user = cls.find_first(id)

        if user.is_admin:
            raise AdminDeactivationNotAllowed()

        User.deactivate(user)
        User.save(user)
