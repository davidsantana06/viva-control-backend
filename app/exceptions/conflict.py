from werkzeug.exceptions import Conflict
from .base.api_exception import ApiException


class DistributorStockAlreadyExists(ApiException, Conflict):
    description = "Stock entry already exists for this product and distributor"


class SkuAlreadyInUse(ApiException, Conflict):
    description = "SKU already in use"


class EmailAlreadyInUse(ApiException, Conflict):
    description = "Email already in use"
