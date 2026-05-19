from flask_restx.fields import Integer, String

from app.dtos import CreateUserDto, UpdateUserDto, UserDto, timestamp_mixin
from app.types import UserRole

from . import user_ns


user_model = user_ns.model(
    "User",
    UserDto(
        id=Integer(readonly=True),
        distributor_id=Integer(),
        name=String(),
        email=String(),
        role=String(enum=list(UserRole)),
        **timestamp_mixin,
    ),
)

create_user_model = user_ns.model(
    "CreateUser",
    CreateUserDto(
        distributor_id=Integer(),
        name=String(required=True, min_length=2, max_length=50),
        email=String(required=True, min_length=5, max_length=255),
        password=String(required=True, min_length=8, max_length=40),
        role=String(required=True, enum=[UserRole.DISTRIBUTOR, UserRole.SELLER]),
    ),
)

update_user_model = user_ns.model(
    "UpdateUser",
    UpdateUserDto(
        name=String(min_length=2, max_length=50),
        email=String(min_length=5, max_length=255),
        password=String(min_length=8, max_length=40),
    ),
)
