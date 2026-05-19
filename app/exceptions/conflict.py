from werkzeug.exceptions import Conflict
from .base.api_exception import ApiException


class DistributorStockAlreadyExistsException(ApiException, Conflict):
    description = (
        "A stock entry already exists for this product and distributor. "
        "Update the existing entry instead."
    )
    api_description = "Distributor stock entry already exists"


class SkuAlreadyInUseException(ApiException, Conflict):
    description = (
        "The provided SKU is already in use by another product. "
        "Choose a unique SKU and try again."
    )
    api_description = "SKU already in use"


class EmailAlreadyRegisteredException(ApiException, Conflict):
    description = (
        "The provided email is already registered. "
        "Use a different email or recover the existing account."
    )
    api_description = "Email already registered"
