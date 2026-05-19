from flask_restx import Resource

from app.dtos import AccessTokenDto
from app.exceptions import (
    InvalidCredentialsException,
    InvalidPayloadException,
    UserNotFoundException,
)
from app.facades import Security
from app.services import AuthService

from . import auth_ns
from .models import access_token_model, login_model, token_pair_model


@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.doc("login")
    @auth_ns.expect(login_model)
    @auth_ns.marshal_with(token_pair_model)
    @auth_ns.response(*InvalidPayloadException.get_api_specs())
    @auth_ns.response(*InvalidCredentialsException.get_api_specs())
    def post(self):
        """Authenticate and retrieve an access and refresh token"""
        return AuthService.issue_token_pair(auth_ns.payload)


@auth_ns.route("/refresh")
class Refresh(Resource):
    @auth_ns.doc("refresh", security="Bearer")
    @auth_ns.marshal_with(access_token_model)
    @auth_ns.response(*UserNotFoundException.get_api_specs())
    def post(self):
        """Exchange a refresh token for a new access token"""
        Security.require_refresh_token()
        return AuthService.refresh_access_token(Security.get_identity())
