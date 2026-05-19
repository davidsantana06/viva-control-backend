from werkzeug.exceptions import NotFound
from .base.api_exception import ApiException


_DESCRIPTION = (
    "The requested {} was not found for the provided data. "
    "Check the submitted values and try again."
)

_API_DESCRIPTION = "{} not found"


class CustomerNotFoundException(ApiException, NotFound):
    description = _DESCRIPTION.format("customer")
    api_description = _API_DESCRIPTION.format("Customer")


class DistributorStockNotFoundException(ApiException, NotFound):
    description = _DESCRIPTION.format("distributor stock entry")
    api_description = _API_DESCRIPTION.format("Distributor stock entry")


class PaymentMethodNotFoundException(ApiException, NotFound):
    description = _DESCRIPTION.format("payment method")
    api_description = _API_DESCRIPTION.format("Payment method")


class ProductNotFoundException(ApiException, NotFound):
    description = _DESCRIPTION.format("product")
    api_description = _API_DESCRIPTION.format("Product")


class OrderNotFoundException(ApiException, NotFound):
    description = _DESCRIPTION.format("order")
    api_description = _API_DESCRIPTION.format("Order")


class UserNotFoundException(ApiException, NotFound):
    description = _DESCRIPTION.format("user")
    api_description = _API_DESCRIPTION.format("User")
