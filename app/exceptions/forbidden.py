from werkzeug.exceptions import Forbidden
from .base.api_exception import ApiException


class RoleNotAllowedException(ApiException, Forbidden):
    description = (
        "Your role does not have permission to access this resource. "
        "Contact an administrator if access is required."
    )
    api_description = "User's role not allowed"


class AdminDeletionNotAllowedException(ApiException, Forbidden):
    description = (
        "Administrator accounts cannot be deleted. "
        "Transfer responsibilities before attempting removal."
    )
    api_description = "Admin deletion not allowed"


class OrderDeletionNotAllowedException(ApiException, Forbidden):
    description = (
        "The order cannot be deleted in its current status. "
        "Cancel the order before attempting to delete it."
    )
    api_description = "non-'PENDING' order deletion not allowed"
