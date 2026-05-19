from app.dtos import CreateUserDto, UpdateUserDto
from app.exceptions import AdminDeletionNotAllowed, EmailAlreadyInUse, UserNotFound
from app.models import User
from app.facades import Security
from app.types import FindAllParams, UserFilter


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
    def find_all(params: FindAllParams, user_filter: UserFilter) -> list[User]:
        return User.find_all(params, user_filter)

    @staticmethod
    def find_first(id: int, user_filter: UserFilter) -> User:
        user = User.find_first_by_id(id, user_filter)

        if not user:
            raise UserNotFound()

        return user

    @classmethod
    def update(cls, id: int, dto: UpdateUserDto, user_filter: UserFilter) -> User:
        user = cls.find_first(id, user_filter)
        if dto.get("password"):
            dto["password_hash"] = Security.hash_password(dto.pop("password"))
        user.update(**dto)
        User.save(user)
        return user

    @classmethod
    def delete(cls, id: int, user_filter: UserFilter) -> None:
        user = cls.find_first(id, user_filter)

        if user.is_admin:
            raise AdminDeletionNotAllowed()

        User.delete(user)
