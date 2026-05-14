from werkzeug.exceptions import Unauthorized
from .base.api_exception import ApiException


class InvalidCredentials(ApiException, Unauthorized):
    description = "Invalid email and/or password"
