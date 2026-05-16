from werkzeug.exceptions import Conflict
from .base.api_exception import ApiException


class EmailAlreadyInUse(ApiException, Conflict):
    description = "Email already in use"


class SkuAlreadyInUse(ApiException, Conflict):
    description = "SKU already in use"
