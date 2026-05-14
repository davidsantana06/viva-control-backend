from werkzeug.security import generate_password_hash

from app.dto.user_dtos import CreateUserDto, UpdateUserDto
from app.exceptions import UserEmailAlreadyInUse, UserNotFound
from app.models import UserRepository, User
from app.types import FindAllParams

from .contract.user_service import UserService


class UserServiceImpl(UserService):
    def __init__(self, user_repository: type[UserRepository]) -> None:
        self.__user_repository = user_repository

    def create(self, dto: CreateUserDto) -> User:
        other_user = self.__user_repository.find_first_by_email(dto["email"])

        if other_user:
            raise UserEmailAlreadyInUse()

        dto["password_hash"] = generate_password_hash(dto.pop("password"))
        user = User(**dto)
        self.__user_repository.save(user)
        return user

    def find_all(self, params: FindAllParams) -> list[User]:
        return self.__user_repository.find_all(params)

    def find_first(self, id: int) -> User:
        user = self.__user_repository.find_first_by_id(id)

        if not user:
            raise UserNotFound()

        return user

    def update(self, id: int, dto: UpdateUserDto) -> User:
        user = self.find_first(id)

        if dto.get("password"):
            dto["password_hash"] = generate_password_hash(dto.pop("password"))

        user.update(**dto)
        self.__user_repository.save(user)
        return user

    def deactivate(self, id: int) -> None:
        user = self.find_first(id)
        self.__user_repository.deactivate(user)
        self.__user_repository.save(user)
