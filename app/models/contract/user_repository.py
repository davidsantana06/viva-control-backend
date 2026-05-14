from abc import ABC, abstractmethod
from typing import Self

from app.types import FindAllParams


class UserRepository(ABC):
    @staticmethod
    @abstractmethod
    def save(user: Self) -> None: ...

    @classmethod
    @abstractmethod
    def find_all(cls, params: FindAllParams) -> list[Self]: ...

    @classmethod
    @abstractmethod
    def find_first_by_id(cls, id: int) -> Self | None: ...

    @classmethod
    @abstractmethod
    def find_first_by_email(cls, email: str) -> Self | None: ...

    @classmethod
    @abstractmethod
    def deactivate(cls, user: Self) -> None: ...
