from flask_jwt_extended import jwt_required
from flask_restx import Resource

from app.exceptions import InvalidCredentialsException, InvalidPayloadException
from app.facades import Security
from app.services import AuthService

from . import auth_ns
from .models import access_token_model, login_model


@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.doc("login")
    @auth_ns.expect(login_model)
    @auth_ns.marshal_with(access_token_model)
    @auth_ns.response(*InvalidPayloadException.get_api_specs())
    @auth_ns.response(*InvalidCredentialsException.get_api_specs())
    def post(self):
        """Authenticate and retrieve an access token"""
        return {"access_token": AuthService.login(auth_ns.payload)}


@auth_ns.route("/protected")
class Protected(Resource):
    @auth_ns.doc("protected", security="Bearer")
    @jwt_required()
    def get(self):
        """Protected route example"""
        return {"logged_in_as": Security.get_token_identity()}
