from werkzeug.exceptions import Conflict
from .base.api_exception import ApiException


class UserEmailAlreadyInUse(ApiException, Conflict):
    description = "Email already in use"
