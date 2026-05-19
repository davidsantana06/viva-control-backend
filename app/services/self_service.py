from app.dtos import UpdateUserDto
from app.exceptions import UserNotFoundException
from app.facades import Security
from app.models import User


class SelfService:
    @staticmethod
    def find_first_or_raise(id: int) -> User:
        user = User.find_first_by_id(id)

        if not user:
            raise UserNotFoundException()

        return user

    @classmethod
    def update(cls, id: int, dto: UpdateUserDto) -> User:
        user = cls.find_first_or_raise(id)
        if dto.get("password"):
            dto["password_hash"] = Security.hash_password(dto.pop("password"))
        user.update(**dto)
        User.save(user)
        return user
