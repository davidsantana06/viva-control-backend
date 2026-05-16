from flask_restx import Resource
from http import HTTPStatus

from app.decorators import (
    create_resource,
    delete_resource,
    get_resource,
    list_resource,
    role_required,
    update_resource,
)
from app.exceptions import PaymentMethodNotFound
from app.services import PaymentMethodService
from app.types import UserRole
from app.utils import ApiUtils

from . import payment_method_ns
from .models import (
    create_payment_method_model,
    payment_method_model,
    update_payment_method_model,
)


@payment_method_ns.route("/")
class PaymentMethodList(Resource):
    __find_all_parser = ApiUtils.build_find_all_parser(payment_method_ns)

    @create_resource(
        payment_method_ns,
        create_payment_method_model,
        payment_method_model,
    )
    @role_required(UserRole.ADMIN)
    def post(self):
        """Create a new payment method"""
        return (
            PaymentMethodService.create(payment_method_ns.payload),
            HTTPStatus.CREATED,
        )

    @list_resource(payment_method_ns, __find_all_parser, payment_method_model)
    @role_required(UserRole.ADMIN, UserRole.DISTRIBUTOR, UserRole.SELLER)
    def get(self):
        """Get all payment methods"""
        find_all_params = ApiUtils.build_find_all_params(self.__find_all_parser)
        return PaymentMethodService.find_all(find_all_params)


@payment_method_ns.route("/<int:id>")
@payment_method_ns.param("id", "The payment method identifier")
class PaymentMethod(Resource):
    @get_resource(payment_method_ns, payment_method_model, PaymentMethodNotFound)
    @role_required(UserRole.ADMIN, UserRole.DISTRIBUTOR, UserRole.SELLER)
    def get(self, id: int):
        """Get a payment method by ID"""
        return PaymentMethodService.find_first(id)

    @update_resource(
        payment_method_ns,
        update_payment_method_model,
        payment_method_model,
        PaymentMethodNotFound,
    )
    @role_required(UserRole.ADMIN)
    def patch(self, id: int):
        """Update a payment method by ID"""
        return PaymentMethodService.update(id, payment_method_ns.payload)

    @delete_resource(payment_method_ns, PaymentMethodNotFound)
    @role_required(UserRole.ADMIN)
    def delete(self, id: int):
        """Deactivate a payment method by ID"""
        PaymentMethodService.deactivate(id)
        return "", HTTPStatus.NO_CONTENT
