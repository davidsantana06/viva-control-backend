from werkzeug.exceptions import NotFound
from .base.api_exception import ApiException


class ProductNotFound(ApiException, NotFound):
    description = "Product not found"


class UserNotFound(ApiException, NotFound):
    description = "User not found"
