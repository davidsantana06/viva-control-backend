from werkzeug.exceptions import Conflict

from .base.api_exception import ApiException


class ConflictException(ApiException, Conflict):
    pass


conflict = (Conflict.code, Conflict.description)
