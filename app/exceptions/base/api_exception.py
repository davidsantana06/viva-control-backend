from werkzeug.exceptions import HTTPException
from app.types import ExceptionSpecs


class ApiException(HTTPException):
    code: int
    description: str

    @classmethod
    def get_specs(cls) -> ExceptionSpecs:
        return (cls.code, cls.description)
