from flask_restx.fields import Date, Integer, String

from app.dtos import CreateCustomerDto, CustomerDto, UpdateCustomerDto, timestamp_mixin
from app.types import DocumentType

from . import customer_ns


customer_model = customer_ns.model(
    "Customer",
    CustomerDto(
        id=Integer(readonly=True),
        distributor_id=Integer(readonly=True),
        seller_id=Integer(),
        name=String(),
        document=String(),
        document_type=String(enum=list(DocumentType)),
        phone=String(),
        address=String(),
        birth_date=Date(),
        notes=String(),
        **timestamp_mixin,
    ),
)

create_customer_model = customer_ns.model(
    "CreateCustomer",
    CreateCustomerDto(
        distributor_id=Integer(),
        seller_id=Integer(),
        name=String(required=True, min_length=2, max_length=50),
        document=String(required=True, min_length=11, max_length=14),
        document_type=String(required=True, enum=list(DocumentType)),
        phone=String(max_length=14),
        address=String(),
        birth_date=Date(),
        notes=String(),
    ),
)

update_customer_model = customer_ns.model(
    "UpdateCustomer",
    UpdateCustomerDto(
        name=String(min_length=2, max_length=50),
        phone=String(max_length=14),
        address=String(),
        birth_date=Date(),
        notes=String(),
    ),
)
