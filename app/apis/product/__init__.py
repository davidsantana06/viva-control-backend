from flask_restx import Namespace

product_ns = Namespace(
    "product",
    description="Product related operations",
    path="/products",
    validate=True,
)

from .models import *
from .resources import *
