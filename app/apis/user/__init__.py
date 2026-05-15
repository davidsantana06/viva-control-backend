from flask_restx import Namespace

user_ns = Namespace(
    "user",
    description="User related operations",
    path="/users",
    validate=True,
)

from .user_list import UserList
from .user import User
