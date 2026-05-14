from werkzeug.exceptions import NotFound
from .base.api_exception import ApiException


class UserNotFound(ApiException, NotFound):
    description = "User not found"
