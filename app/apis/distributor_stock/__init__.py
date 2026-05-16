from flask_restx import Namespace

distributor_stock_ns = Namespace(
    "distributor_stock",
    description="Distributor stock related operations",
    path="/distributor-stocks",
    validate=True,
)

from .models import *
from .resources import *
