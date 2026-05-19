from flask_restx import Resource
from http import HTTPStatus

from app.decorators import (
    auth_required,
    create_resource,
    delete_resource,
    get_resource,
    list_resource,
    update_resource,
)
from app.exceptions import EmailAlreadyInUse, UserNotFound
from app.factories import FindAllFactory, UserFilterFactory
from app.services import UserService
from app.types import CurrentUser, UserRole

from . import user_ns
from .models import create_user_model, update_user_model, user_model


@user_ns.route("/")
class UserListResource(Resource):
    __find_all_parser = FindAllFactory.build_find_all_parser(user_ns)

    @create_resource(
        user_ns,
        create_user_model,
        user_model,
        EmailAlreadyInUse,
    )
    @auth_required(UserRole.ADMIN)
    def post(self, **_):
        """Create a new user"""
        return UserService.create(user_ns.payload), HTTPStatus.CREATED

    @list_resource(user_ns, __find_all_parser, user_model)
    @auth_required(UserRole.ADMIN, UserRole.DISTRIBUTOR)
    def get(self, current_user: CurrentUser):
        """Get all users"""
        find_all_params = FindAllFactory.build_find_all_params(self.__find_all_parser)
        user_filter = UserFilterFactory.build_distributor_filter(current_user)
        return UserService.find_all(find_all_params, user_filter)


@user_ns.route("/<int:id>")
@user_ns.param("id", "The user identifier")
class UserResource(Resource):
    @get_resource(user_ns, user_model, UserNotFound)
    @auth_required(UserRole.ADMIN, UserRole.DISTRIBUTOR)
    def get(self, id: int, current_user: CurrentUser):
        """Get a user by ID"""
        user_filter = UserFilterFactory.build_distributor_filter(current_user)
        return UserService.find_first_or_raise(id, user_filter)

    @update_resource(
        user_ns,
        update_user_model,
        user_model,
        UserNotFound,
        EmailAlreadyInUse,
    )
    @auth_required(UserRole.ADMIN)
    def patch(self, id: int, current_user: CurrentUser):
        """Update a user by ID"""
        user_filter = UserFilterFactory.build_distributor_filter(current_user)
        return UserService.update(id, user_ns.payload, user_filter)

    @delete_resource(user_ns, UserNotFound)
    @auth_required(UserRole.ADMIN)
    def delete(self, id: int, current_user: CurrentUser):
        """Delete a user by ID"""
        user_filter = UserFilterFactory.build_distributor_filter(current_user)
        UserService.delete(id, user_filter)
        return "", HTTPStatus.NO_CONTENT
