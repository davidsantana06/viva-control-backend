from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Object, Provider

from app.models.contract.user_repository import UserRepository
from app.models.user import User
from app.services.contract.user_service import UserService
from app.services.user_service_impl import UserServiceImpl


class Container(DeclarativeContainer):
    user_repository: Provider[type[UserRepository]] = Object(User)
    user_service: Provider[UserService] = Factory(UserServiceImpl, user_repository=user_repository)
