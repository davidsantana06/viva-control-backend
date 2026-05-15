from functools import wraps
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request

from app.exceptions import RoleNotAllowed
from app.types import UserRole
from app.utils import ApiUtils


def roles_required(*roles: UserRole):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            id, role = get_jwt_identity(), claims["role"]

            role_not_allowed = role not in roles
            if role_not_allowed:
                raise RoleNotAllowed()

            ApiUtils.bind_current_user(int(id), role)
            return func(*args, **kwargs)

        return wrapper

    return decorator


distributor_required = roles_required(UserRole.DISTRIBUTOR)
