from flask_restx import Namespace

customer_ns = Namespace(
    "customer",
    description="Customer related operations",
    path="/customers",
    validate=True,
)

from .models import *
from .resources import *
