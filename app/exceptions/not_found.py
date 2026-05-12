from werkzeug.exceptions import NotFound

from .base.api_exception import ApiException


class NotFoundException(ApiException, NotFound):
    pass


not_found = (NotFound.code, NotFound.description)
