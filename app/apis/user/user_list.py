from flask_restx import Resource
from http import HTTPStatus

from app.dtos import create_user_dto, user_dto
from app.exceptions import InvalidPayload
from app.services import UserService
from app.utils.api_specs import parse_find_all_args, set_find_all_parser
from . import user_ns


@user_ns.route("/")
class UserList(Resource):
    __find_all_parser = set_find_all_parser(user_ns)

    @user_ns.doc("create_user")
    @user_ns.expect(create_user_dto)
    @user_ns.marshal_with(user_dto, code=HTTPStatus.CREATED)
    @user_ns.response(*InvalidPayload.get_specs())
    def post(self):
        """Create a new user"""
        return UserService.create(user_ns.payload), HTTPStatus.CREATED

    @user_ns.doc("list_users")
    @user_ns.expect(__find_all_parser)
    @user_ns.marshal_list_with(user_dto)
    def get(self):
        """Get all users"""
        find_all_params = parse_find_all_args(self.__find_all_parser)
        return UserService.find_all(find_all_params)
