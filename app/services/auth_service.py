from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from app.dtos import LoginDto
from app.exceptions import InvalidCredentials
from app.models import User


def login(dto: LoginDto) -> str:
    user = User.find_first_by_email(dto["email"])

    user_is_inactive = not user or not user.is_active
    invalid_password = not check_password_hash(user.password_hash, dto["password"])
    if user_is_inactive or invalid_password:
        raise InvalidCredentials()

    return create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role},
    )
