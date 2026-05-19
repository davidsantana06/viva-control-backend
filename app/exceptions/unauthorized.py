from werkzeug.exceptions import Unauthorized
from .base.api_exception import ApiException


class InvalidCredentialsException(ApiException, Unauthorized):
    description = (
        "The provided credentials are incorrect. "
        "Verify your data and try again."
    )
    api_description = "Invalid credentials"
