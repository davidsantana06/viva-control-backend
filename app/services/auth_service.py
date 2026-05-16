from app.dtos import LoginDto
from app.exceptions import InvalidCredentials
from app.facades import Security
from app.models import User


class AuthService:
    @staticmethod
    def login(dto: LoginDto) -> str:
        user = User.find_first_by_email(dto["email"])

        user_is_inactive = not user or not user.is_active
        invalid_password = not Security.verify_password(user.password_hash, dto["password"])
        if user_is_inactive or invalid_password:
            raise InvalidCredentials()

        return Security.issue_token(user)
