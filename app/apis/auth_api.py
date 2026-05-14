from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource

from app.dto.auth_dtos import login_dto, access_token_dto
from app.exceptions import InvalidCredentials, InvalidPayload
from app.services import auth_service


auth_ns = Namespace(
    "auth",
    description="Authentication operations",
    path="/auth",
    validate=True,
)


@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.doc("login")
    @auth_ns.expect(login_dto)
    @auth_ns.marshal_with(access_token_dto)
    @auth_ns.response(*InvalidPayload.get_specs())
    @auth_ns.response(*InvalidCredentials.get_specs())
    def post(self):
        """Authenticate and retrieve an access token"""
        return {"access_token": auth_service.login(auth_ns.payload)}


@auth_ns.route("/protected")
class Protected(Resource):
    @auth_ns.doc("protected", security="Bearer")
    @jwt_required()
    def get(self):
        """Protected route example"""
        return {"logged_in_as": get_jwt_identity()}
