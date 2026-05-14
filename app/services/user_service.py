from werkzeug.security import generate_password_hash

from app.dto.user_dtos import CreateUserDto, UpdateUserDto
from app.exceptions import UserEmailAlreadyInUse, UserNotFound
from app.models import User
from app.types import FindAllParams


def create(dto: CreateUserDto) -> User:
    if User.find_first_by_email(dto["email"]):
        raise UserEmailAlreadyInUse()

    dto["password_hash"] = generate_password_hash(dto.pop("password"))
    user = User(**dto)
    User.save(user)
    return user


def find_all(params: FindAllParams) -> list[User]:
    return User.find_all(params)


def find_first(id: int) -> User:
    user = User.find_first_by_id(id)

    if not user:
        raise UserNotFound()

    return user


def update(id: int, dto: UpdateUserDto) -> User:
    user = find_first(id)

    if dto.get("password"):
        dto["password_hash"] = generate_password_hash(dto.pop("password"))

    user.update(**dto)
    User.save(user)
    return user


def deactivate(id: int) -> None:
    user = find_first(id)
    User.deactivate(user)
    User.save(user)
