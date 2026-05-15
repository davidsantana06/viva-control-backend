from flask_restx.fields import String
from app.dtos import AccessTokenDto, LoginDto
from . import auth_ns


login_model = auth_ns.model(
    "Login",
    LoginDto(
        email=String(required=True, min_length=5, max_length=255),
        password=String(required=True, min_length=8, max_length=40),
    ),
)

access_token_model = auth_ns.model(
    "AccessToken",
    AccessTokenDto(
        access_token=String(),
    ),
)
