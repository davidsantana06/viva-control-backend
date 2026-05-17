from app.dtos import CreateUserDto, UpdateUserDto
from app.exceptions import AdminDeactivationNotAllowed, EmailAlreadyInUse, UserNotFound
from app.factories import UserFilterFactory
from app.models import User
from app.facades import Security
from app.types import CurrentUser, FindAllParams


class UserService:
    @staticmethod
    def create(dto: CreateUserDto) -> User:
        other_user = User.find_first_by_email(dto["email"])
        if other_user:
            raise EmailAlreadyInUse()

        dto["password_hash"] = Security.hash_password(dto.pop("password"))
        user = User(**dto)
        User.save(user)
        return user

    @staticmethod
    def find_all(params: FindAllParams, current_user: CurrentUser) -> list[User]:
        user_filter = UserFilterFactory.build_distributor_filter(current_user)
        return User.find_all(params, user_filter)

    @staticmethod
    def find_first(id: int, current_user: CurrentUser) -> User:
        user_filter = UserFilterFactory.build_distributor_filter(current_user)
        user = User.find_first_by_id(id, user_filter)

        if not user:
            raise UserNotFound()

        return user

    @classmethod
    def update(cls, id: int, dto: UpdateUserDto, current_user: CurrentUser) -> User:
        user = cls.find_first(id, current_user)
        if dto.get("password"):
            dto["password_hash"] = Security.hash_password(dto.pop("password"))
        user.update(**dto)
        User.save(user)
        return user

    @classmethod
    def deactivate(cls, id: int, current_user: CurrentUser) -> None:
        user = cls.find_first(id, current_user)

        if user.is_admin:
            raise AdminDeactivationNotAllowed()

        User.deactivate(user)
        User.save(user)
