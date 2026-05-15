from flask_restx import Namespace

auth_ns = Namespace(
    "auth",
    description="Authentication operations",
    path="/auth",
    validate=True,
)

from .login import Login
from .protected import Protected
