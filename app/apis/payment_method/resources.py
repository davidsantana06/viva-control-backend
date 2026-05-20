from flask_restx import Resource
from http import HTTPStatus

from app.decorators import (
    auth_required,
    create_resource,
    delete_resource,
    get_resource,
    list_resource,
    update_resource,
)
from app.exceptions import PaymentMethodNotFoundException
from app.factories import FindAllFactory
from app.services import PaymentMethodService
from app.types import UserRole

from . import payment_method_ns
from .models import (
    create_payment_method_model,
    payment_method_model,
    update_payment_method_model,
)


@payment_method_ns.route("/")
class PaymentMethodListResource(Resource):
    __find_all_parser = FindAllFactory.build_find_all_parser(payment_method_ns)

    @create_resource(
        payment_method_ns,
        create_payment_method_model,
        payment_method_model,
    )
    @auth_required(UserRole.ADMIN)
    def post(self, **_):
        """Create a new payment method"""
        return (
            PaymentMethodService.create(payment_method_ns.payload),
            HTTPStatus.CREATED,
        )

    @list_resource(payment_method_ns, __find_all_parser, payment_method_model)
    @auth_required(UserRole.ADMIN, UserRole.DISTRIBUTOR, UserRole.SELLER)
    def get(self, **_):
        """Get all payment methods"""
        find_all_params = FindAllFactory.build_find_all_params(self.__find_all_parser)
        return PaymentMethodService.find_all(find_all_params)


@payment_method_ns.route("/<int:id>")
@payment_method_ns.param("id", "The payment method identifier")
class PaymentMethodResource(Resource):
    @get_resource(payment_method_ns, payment_method_model, PaymentMethodNotFoundException)
    @auth_required(UserRole.ADMIN, UserRole.DISTRIBUTOR, UserRole.SELLER)
    def get(self, id: int, **_):
        """Get a payment method by ID"""
        return PaymentMethodService.find_first_or_raise(id)

    @update_resource(
        payment_method_ns,
        update_payment_method_model,
        payment_method_model,
        PaymentMethodNotFoundException,
    )
    @auth_required(UserRole.ADMIN)
    def patch(self, id: int, **_):
        """Update a payment method by ID"""
        return PaymentMethodService.update(id, payment_method_ns.payload)

    @delete_resource(payment_method_ns, PaymentMethodNotFoundException)
    @auth_required(UserRole.ADMIN)
    def delete(self, id: int, **_):
        """Delete a payment method by ID"""
        PaymentMethodService.delete(id)
        return "", HTTPStatus.NO_CONTENT
