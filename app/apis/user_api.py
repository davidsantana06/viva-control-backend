from flask_restx import Namespace, Resource
from http import HTTPStatus

from app.dto.user_dtos import create_user_dto, update_user_dto, user_dto
from app.exceptions import InvalidPayload, UserNotFound
from app.services import user_service
from app.utils.api_specs import parse_find_all_args, set_find_all_parser


user_ns = Namespace(
    "user",
    description="User related operations",
    path="/users",
    validate=True,
)


@user_ns.route("/")
class UserList(Resource):
    __find_all_parser = set_find_all_parser(user_ns)

    @user_ns.doc("create_user")
    @user_ns.expect(create_user_dto)
    @user_ns.marshal_with(user_dto, code=HTTPStatus.CREATED)
    @user_ns.response(*InvalidPayload.get_specs())
    def post(self):
        """Create a new user"""
        return user_service.create(user_ns.payload), HTTPStatus.CREATED

    @user_ns.doc("list_users")
    @user_ns.expect(__find_all_parser)
    @user_ns.marshal_list_with(user_dto)
    def get(self):
        """Get all users"""
        find_all_params = parse_find_all_args(self.__find_all_parser)
        return user_service.find_all(find_all_params)


@user_ns.route("/<int:id>")
@user_ns.param("id", "The user identifier")
@user_ns.response(*UserNotFound.get_specs())
class User(Resource):
    @user_ns.doc("get_user")
    @user_ns.marshal_with(user_dto)
    def get(self, id: int):
        """Get a user by ID"""
        return user_service.find_first(id)

    @user_ns.doc("update_user")
    @user_ns.expect(update_user_dto)
    @user_ns.marshal_with(user_dto)
    @user_ns.response(*InvalidPayload.get_specs())
    def put(self, id: int):
        """Update a user by ID"""
        return user_service.update(id, user_ns.payload)

    @user_ns.doc("deactivate_user")
    @user_ns.response(HTTPStatus.NO_CONTENT, "Success")
    def delete(self, id: int):
        """Deactivate a user by ID"""
        user_service.deactivate(id)
        return "", HTTPStatus.NO_CONTENT
