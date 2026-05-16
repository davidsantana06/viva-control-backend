from werkzeug.exceptions import NotFound
from .base.api_exception import ApiException


class PaymentMethodNotFound(ApiException, NotFound):
    description = "Payment method not found"


class ProductNotFound(ApiException, NotFound):
    description = "Product not found"


class UserNotFound(ApiException, NotFound):
    description = "User not found"
