from abc import ABC, abstractmethod

from app.dto.user_dtos import CreateUserDto, UpdateUserDto
from app.models import User
from app.types import FindAllParams


class UserService(ABC):
    @abstractmethod
    def create(self, dto: CreateUserDto) -> User: ...

    @abstractmethod
    def find_all(self, params: FindAllParams) -> list[User]: ...

    @abstractmethod
    def find_first(self, id: int) -> User: ...

    @abstractmethod
    def update(self, id: int, dto: UpdateUserDto) -> User: ...

    @abstractmethod
    def deactivate(self, id: int) -> None: ...
