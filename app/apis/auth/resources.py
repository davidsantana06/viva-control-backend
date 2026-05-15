from flask_jwt_extended import jwt_required
from flask_restx import Resource

from app.exceptions import InvalidCredentials, InvalidPayload
from app.proxies import JwtProxy
from app.services import AuthService

from . import auth_ns
from .models import access_token_model, login_model


@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.doc("login")
    @auth_ns.expect(login_model)
    @auth_ns.marshal_with(access_token_model)
    @auth_ns.response(*InvalidPayload.get_specs())
    @auth_ns.response(*InvalidCredentials.get_specs())
    def post(self):
        """Authenticate and retrieve an access token"""
        return {"access_token": AuthService.login(auth_ns.payload)}


@auth_ns.route("/protected")
class Protected(Resource):
    @auth_ns.doc("protected", security="Bearer")
    @jwt_required()
    def get(self):
        """Protected route example"""
        return {"logged_in_as": JwtProxy.get_identity()}
