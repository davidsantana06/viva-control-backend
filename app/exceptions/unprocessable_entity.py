from werkzeug.exceptions import UnprocessableEntity
from .base.api_exception import ApiException


class DelinquentCustomerException(ApiException, UnprocessableEntity):
    description = (
        "The customer has an overdue unpaid order. "
        "Settle the pending payment before placing a new order."
    )
    api_description = "Delinquent customer"


class InvalidPayloadException(ApiException, UnprocessableEntity):
    description = (
        "The request payload is invalid or missing required fields. "
        "Review the submitted data and try again."
    )
    api_description = "Invalid request payload"


class InvalidOrderStatusTransitionException(ApiException, UnprocessableEntity):
    description = (
        "The requested status transition is not allowed for the current state. "
        "Consult the valid transitions and try again."
    )
    api_description = "Invalid status transition"
