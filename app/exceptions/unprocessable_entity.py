from werkzeug.exceptions import UnprocessableEntity
from .base.api_exception import ApiException


class DelinquentCustomer(ApiException, UnprocessableEntity):
    description = "Order blocked. Customer has an overdue payment."


class InvalidPayload(ApiException, UnprocessableEntity):
    description = "Invalid payload"


class OrderStatusTransitionInvalid(ApiException, UnprocessableEntity):
    description = "Invalid status transition"
