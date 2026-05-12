from werkzeug.exceptions import UnprocessableEntity
from .base.api_exception import ApiException


class InvalidPayload(ApiException, UnprocessableEntity):
    description = "Invalid payload"
