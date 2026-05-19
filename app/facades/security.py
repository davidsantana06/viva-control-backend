from flask_jwt_extended import (
    create_access_token,
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
    def issue_jwt(user: User) -> str:
        identity = str(user.id)
        return create_access_token(
            identity,
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
    def require_jwt() -> None:
        verify_jwt_in_request()

    @staticmethod
    def get_jwt_identity() -> int:
        identity = get_jwt_identity()
        return int(identity)

    @staticmethod
    def get_jwt_claims() -> JwtClaims:
        return get_jwt()
