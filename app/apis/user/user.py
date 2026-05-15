from flask_restx import Resource
from http import HTTPStatus

from app.dto.user_dtos import update_user_dto, user_dto
from app.exceptions import InvalidPayload, UserNotFound
from app.services import user_service
from . import user_ns


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
