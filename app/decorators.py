from functools import wraps

from app.exceptions import RoleNotAllowed
from app.proxies import JwtProxy
from app.types import CurrentUser, UserRole
from app.utils import ApiUtils


def role_required(*roles: UserRole):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            JwtProxy.verify_or_raise()
            claims = JwtProxy.get_claims()

            role_not_allowed = claims["role"] not in roles
            if role_not_allowed:
                raise RoleNotAllowed()

            current_user = CurrentUser(JwtProxy.get_identity(), claims["role"])
            ApiUtils.bind_current_user(current_user)
            return func(*args, **kwargs)
        return wrapper
    return decorator
