from werkzeug.exceptions import Conflict
from .base.api_exception import ApiException


class ProductSkuAlreadyInUse(ApiException, Conflict):
    description = "SKU already in use"


class UserEmailAlreadyInUse(ApiException, Conflict):
    description = "Email already in use"
