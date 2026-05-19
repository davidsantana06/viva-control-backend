from flask_restx import Namespace

user_ns = Namespace(
    "user",
    description="User management operations",
    path="/",
    validate=True,
)

from ._self.resources import *
from .distributor.resources import *
from .seller.resources import *

from .models import *
