from flask_restx.fields import Integer, String

from app.dtos import CreatePaymentMethodDto, PaymentMethodDto, UpdatePaymentMethodDto, timestamp_mixin

from . import payment_method_ns


payment_method_model = payment_method_ns.model(
    "PaymentMethod",
    PaymentMethodDto(
        id=Integer(readonly=True),
        name=String(),
        **timestamp_mixin,
    ),
)

create_payment_method_model = payment_method_ns.model(
    "CreatePaymentMethod",
    CreatePaymentMethodDto(
        name=String(required=True, min_length=2, max_length=50),
    ),
)

update_payment_method_model = payment_method_ns.model(
    "UpdatePaymentMethod",
    UpdatePaymentMethodDto(
        name=String(min_length=2, max_length=50),
    ),
)
