from flask_restx.fields import Float, Integer

from app.dtos import (
    CreateDistributorStockDto,
    DistributorStockDto,
    UpdateDistributorStockDto,
    timestamp_mixin,
)

from . import distributor_stock_ns


distributor_stock_model = distributor_stock_ns.model(
    "DistributorStock",
    DistributorStockDto(
        id=Integer(readonly=True),
        product_id=Integer(readonly=True),
        distributor_id=Integer(readonly=True),
        current_quantity=Float(),
        minimum_quantity=Float(),
        **timestamp_mixin,
    ),
)

create_distributor_stock_model = distributor_stock_ns.model(
    "CreateDistributorStock",
    CreateDistributorStockDto(
        product_id=Integer(required=True),
        current_quantity=Float(required=True),
        minimum_quantity=Float(),
    ),
)

update_distributor_stock_model = distributor_stock_ns.model(
    "UpdateDistributorStock",
    UpdateDistributorStockDto(
        current_quantity=Float(),
        minimum_quantity=Float(),
    ),
)
