from app.dtos import LoginDto
from app.exceptions import InvalidCredentials
from app.facades import Security
from app.models import User


class AuthService:
    @staticmethod
    def login(dto: LoginDto) -> str:
        user = User.find_first_by_email(dto["email"])

        invalid_credentials = not user or not Security.verify_password(
            user.password_hash,
            dto["password"]
        )
        if invalid_credentials:
            raise InvalidCredentials()

        return Security.issue_token(user)
