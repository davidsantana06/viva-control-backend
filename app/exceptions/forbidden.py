from werkzeug.exceptions import Forbidden
from .base.api_exception import ApiException


class RoleNotAllowed(ApiException, Forbidden):
    description = "Role not allowed"
