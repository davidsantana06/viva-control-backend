from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    verify_jwt_in_request,
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.models import User
from app.types import JwtClaims, JwtUser


class Security:
    @staticmethod
    def hash_password(password: str) -> str:
        return generate_password_hash(password, method="scrypt", salt_length=16)

    @staticmethod
    def verify_password(password_hash: str, password: str) -> bool:
        return check_password_hash(password_hash, password)

    @staticmethod
    def issue_access_token(user: User) -> str:
        return create_access_token(
            str(user.id),
            additional_claims={
                "user": JwtUser(
                    distributor_id=user.distributor_id,
                    name=user.name,
                    role=user.role,
                    is_admin=user.is_admin,
                    is_distributor=user.is_distributor,
                    is_seller=user.is_seller,
                ),
            },
        )

    @staticmethod
    def issue_refresh_token(user: User) -> str:
        return create_refresh_token(str(user.id))

    @staticmethod
    def require_access_token() -> None:
        verify_jwt_in_request()

    @staticmethod
    def require_refresh_token() -> None:
        verify_jwt_in_request(refresh=True)

    @staticmethod
    def get_identity() -> int:
        return int(get_jwt_identity())

    @staticmethod
    def get_claims() -> JwtClaims:
        return get_jwt()
