from werkzeug.exceptions import Forbidden
from .base.api_exception import ApiException


class AdminDeactivationNotAllowed(ApiException, Forbidden):
    description = "Admin user cannot be deactivated"


class RoleNotAllowed(ApiException, Forbidden):
    description = "User's role is not allowed to access this resource"
