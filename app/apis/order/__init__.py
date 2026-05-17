from flask_restx import Namespace

order_ns = Namespace(
    "order",
    description="Order related operations",
    path="/orders",
    validate=True,
)

from .models import *
from .resources import *
