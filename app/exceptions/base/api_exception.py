from werkzeug.exceptions import HTTPException


class ApiException(HTTPException):
    code: int
    description: str

    @classmethod
    def get_response(cls) -> tuple[int, str]:
        return (cls.code, cls.description)
