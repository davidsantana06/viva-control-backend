from flask_restx.fields import Date, Float, Integer, List, Nested, String

from app.dtos import (
    CreateOrderDto,
    CreateOrderItemDto,
    OrderDto,
    OrderItemDto,
    UpdateOrderStatusDto,
    lifecycle_mixin,
    timestamp_mixin,
)
from app.types import OrderStatus

from . import order_ns


order_item_model = order_ns.model(
    "OrderItem",
    OrderItemDto(
        id=Integer(readonly=True),
        order_id=Integer(readonly=True),
        product_id=Integer(),
        quantity=Integer(),
        unit_price=Float(),
        total_price=Float(readonly=True),
        **timestamp_mixin,
    ),
)

order_model = order_ns.model(
    "Order",
    OrderDto(
        id=Integer(readonly=True),
        customer_id=Integer(),
        distributor_id=Integer(readonly=True),
        seller_id=Integer(),
        payment_method_id=Integer(),
        total_amount=Float(readonly=True),
        discount_pct=Integer(),
        discount_amount=Float(readonly=True),
        net_amount=Float(readonly=True),
        payment_installments=Integer(),
        payment_due_date=Date(),
        notes=String(),
        status=String(enum=list(OrderStatus), readonly=True),
        items=List(Nested(order_item_model)),
        **lifecycle_mixin,
    ),
)

create_order_item_model = order_ns.model(
    "CreateOrderItem",
    CreateOrderItemDto(
        product_id=Integer(required=True),
        quantity=Integer(required=True),
        unit_price=Float(required=True),
    ),
)

create_order_model = order_ns.model(
    "CreateOrder",
    CreateOrderDto(
        customer_id=Integer(required=True),
        payment_method_id=Integer(),
        discount_pct=Integer(required=True, min=0, max=100),
        payment_installments=Integer(required=True, min=1, max=10),
        payment_due_date=Date(required=True),
        notes=String(),
        items=List(Nested(create_order_item_model), required=True),
    ),
)

update_order_status_model = order_ns.model(
    "UpdateOrderStatus",
    UpdateOrderStatusDto(
        status=String(required=True, enum=list(OrderStatus)),
    ),
)
