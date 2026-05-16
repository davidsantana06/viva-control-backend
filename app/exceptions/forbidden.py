from werkzeug.exceptions import Forbidden
from .base.api_exception import ApiException


class UserAdminDeactivationNotAllowed(ApiException, Forbidden):
    description = "Admin user deactivation not allowed"


class UserRoleNotAllowed(ApiException, Forbidden):
    description = "User role not allowed"
