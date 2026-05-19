from werkzeug.exceptions import HTTPException
from app.types import ExceptionSpecs


class ApiException(HTTPException):
    api_description: str

    @classmethod
    def get_api_specs(cls) -> ExceptionSpecs:
        return cls.code, cls.api_description
