from abc import ABC, abstractmethod
from typing import Self

from app.types import SortOrder


class UserRepository(ABC):
    @classmethod
    @abstractmethod
    def create(cls, user: Self) -> None: ...

    @classmethod
    @abstractmethod
    def find_first(cls, id: int) -> Self | None: ...

    @classmethod
    @abstractmethod
    def find_all(
        cls,
        q: str | None = None,
        order: SortOrder = "ASC",
        sort: str = "id",
        page: int = 1,
        per_page: int = 10,
    ) -> list[Self]: ...

    @classmethod
    @abstractmethod
    def deactivate(cls, user: Self) -> None: ...
