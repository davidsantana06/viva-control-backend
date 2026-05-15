from flask_restx.fields import Float, Integer, String

from app.dtos import CreateProductDto, ProductDto, UpdateProductDto, lifecycle_mixin

from . import product_ns


product_model = product_ns.model(
    "Product",
    ProductDto(
        id=Integer(readonly=True),
        name=String(),
        sku=String(),
        description=String(),
        suggested_price=Float(),
        **lifecycle_mixin,
    ),
)

create_product_model = product_ns.model(
    "CreateProduct",
    CreateProductDto(
        name=String(required=True, min_length=2, max_length=100),
        sku=String(required=True, min_length=1, max_length=50),
        description=String(),
        suggested_price=Float(required=True),
    ),
)

update_product_model = product_ns.model(
    "UpdateProduct",
    UpdateProductDto(
        name=String(min_length=2, max_length=100),
        sku=String(min_length=1, max_length=50),
        description=String(),
        suggested_price=Float(),
    ),
)
