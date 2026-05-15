from werkzeug.security import check_password_hash

from app.dtos import LoginDto
from app.exceptions import InvalidCredentials
from app.proxies import JwtProxy
from app.models import User


class AuthService:
    @staticmethod
    def login(dto: LoginDto) -> str:
        user = User.find_first_by_email(dto["email"])

        user_is_inactive = not user or not user.is_active
        invalid_password = not check_password_hash(user.password_hash, dto["password"])
        if user_is_inactive or invalid_password:
            raise InvalidCredentials()

        return JwtProxy.issue(user)
