from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    verify_jwt_in_request,
)

from app.models import User
from app.types import JwtClaims


class JwtProxy:
    @staticmethod
    def issue(user: User) -> str:
        return create_access_token(
            identity=str(user.id),
            additional_claims=JwtClaims(
                parent_id=user.parent_id,
                name=user.name,
                role=user.role,
                is_admin=user.is_admin,
                is_distributor=user.is_distributor,
                is_seller=user.is_seller,
            ),
        )

    @staticmethod
    def verify_or_raise() -> None:
        verify_jwt_in_request()

    @staticmethod
    def get_identity() -> int:
        return int(get_jwt_identity())

    @staticmethod
    def get_claims() -> JwtClaims:
        return get_jwt()
