from flask_restx import Resource

from app.dtos import access_token_dto, login_dto
from app.exceptions import InvalidCredentials, InvalidPayload
from app.services import AuthService
from . import auth_ns


@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.doc("login")
    @auth_ns.expect(login_dto)
    @auth_ns.marshal_with(access_token_dto)
    @auth_ns.response(*InvalidPayload.get_specs())
    @auth_ns.response(*InvalidCredentials.get_specs())
    def post(self):
        """Authenticate and retrieve an access token"""
        return {"access_token": AuthService.login(auth_ns.payload)}
