from werkzeug.exceptions import Forbidden
from .base.api_exception import ApiException


class RoleNotAllowed(ApiException, Forbidden):
    description = "User's role is not allowed to access this resource"


class AdminDeletionNotAllowed(ApiException, Forbidden):
    description = "Admin user cannot be deleted"


class OrderDeletionNotAllowed(ApiException, Forbidden):
    description = "Only cancelled orders can be deleted"
