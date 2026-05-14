from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Object, Provider

from app.models.contract.user_repository import UserRepository
from app.models.user import User


class Container(DeclarativeContainer):
    user_repository: Provider[ type[UserRepository] ] = Object(User)
