from flask_restx import Resource
from http import HTTPStatus

from app.exceptions import InvalidPayload, UserNotFound
from app.services import UserService
from app.utils import ApiUtils

from . import user_ns
from .models import create_user_model, update_user_model, user_model


@user_ns.route("/")
class UserList(Resource):
    __find_all_parser = ApiUtils.build_find_all_parser(user_ns)

    @user_ns.doc("create_user")
    @user_ns.expect(create_user_model)
    @user_ns.marshal_with(user_model, code=HTTPStatus.CREATED)
    @user_ns.response(*InvalidPayload.get_specs())
    def post(self):
        """Create a new user"""
        return UserService.create(user_ns.payload), HTTPStatus.CREATED

    @user_ns.doc("list_users")
    @user_ns.expect(__find_all_parser)
    @user_ns.marshal_list_with(user_model)
    def get(self):
        """Get all users"""
        find_all_params = ApiUtils.build_find_all_params(self.__find_all_parser)
        return UserService.find_all(find_all_params)


@user_ns.route("/<int:id>")
@user_ns.param("id", "The user identifier")
@user_ns.response(*UserNotFound.get_specs())
class User(Resource):
    @user_ns.doc("get_user")
    @user_ns.marshal_with(user_model)
    def get(self, id: int):
        """Get a user by ID"""
        return UserService.find_first(id)

    @user_ns.doc("update_user")
    @user_ns.expect(update_user_model)
    @user_ns.marshal_with(user_model)
    @user_ns.response(*InvalidPayload.get_specs())
    def patch(self, id: int):
        """Update a user by ID"""
        return UserService.update(id, user_ns.payload)

    @user_ns.doc("deactivate_user")
    @user_ns.response(HTTPStatus.NO_CONTENT, "Success")
    def delete(self, id: int):
        """Deactivate a user by ID"""
        UserService.deactivate(id)
        return "", HTTPStatus.NO_CONTENT
