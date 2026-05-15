from flask_restx import Namespace

user_ns = Namespace(
    "user",
    description="User related operations",
    path="/users",
    validate=True,
)

from .models import *
from .resources import *
