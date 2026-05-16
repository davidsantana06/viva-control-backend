from flask_restx import Resource
from http import HTTPStatus

from app.decorators import (
    create_resource,
    deactivate_resource,
    get_resource,
    list_resource,
    role_required,
    update_resource,
)
from app.exceptions import EmailAlreadyInUse, UserNotFound
from app.services import UserService
from app.types import UserRole
from app.utils import ApiUtils

from . import user_ns
from .models import create_user_model, update_user_model, user_model


@user_ns.route("/")
class UserList(Resource):
    __find_all_parser = ApiUtils.build_find_all_parser(user_ns)

    @create_resource(
        user_ns,
        create_user_model,
        user_model,
        EmailAlreadyInUse,
    )
    @role_required(UserRole.ADMIN)
    def post(self):
        """Create a new user"""
        return UserService.create(user_ns.payload), HTTPStatus.CREATED

    @list_resource(user_ns, __find_all_parser, user_model)
    @role_required(UserRole.ADMIN, UserRole.DISTRIBUTOR)
    def get(self):
        """Get all users"""
        current_user = ApiUtils.resolve_current_user()
        find_all_params = ApiUtils.build_find_all_params(self.__find_all_parser)
        return UserService.find_all(find_all_params, current_user)


@user_ns.route("/<int:id>")
@user_ns.param("id", "The user identifier")
class User(Resource):
    @get_resource(user_ns, user_model, UserNotFound)
    @role_required(UserRole.ADMIN, UserRole.DISTRIBUTOR)
    def get(self, id: int):
        """Get a user by ID"""
        current_user = ApiUtils.resolve_current_user()
        return UserService.find_first(id, current_user)

    @update_resource(
        user_ns,
        update_user_model,
        user_model,
        UserNotFound,
        EmailAlreadyInUse,
    )
    @role_required(UserRole.ADMIN)
    def patch(self, id: int):
        """Update a user by ID"""
        current_user = ApiUtils.resolve_current_user()
        return UserService.update(id, user_ns.payload, current_user)

    @deactivate_resource(user_ns, UserNotFound)
    @role_required(UserRole.ADMIN)
    def delete(self, id: int):
        """Deactivate a user by ID"""
        current_user = ApiUtils.resolve_current_user()
        UserService.deactivate(id, current_user)
        return "", HTTPStatus.NO_CONTENT
