from flask_restx import Namespace

payment_method_ns = Namespace(
    "payment_method",
    description="Payment method related operations",
    path="/payment-methods",
    validate=True,
)

from .models import *
from .resources import *
