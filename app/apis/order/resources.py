from datetime import date
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
from app.exceptions import (
    CustomerNotFound,
    DelinquentCustomer,
    OrderNotFound,
    OrderStatusTransitionInvalid,
    ProductNotFound,
)
from app.factories import FindAllFactory
from app.services import OrderService
from app.types import UserRole
from app.utils import ApiUtils

from . import order_ns
from .models import (
    create_order_model,
    order_model,
    update_order_status_model,
)


@order_ns.route("/")
class OrderList(Resource):
    __find_all_parser = FindAllFactory.build_user_scoped_find_all_parser(order_ns)

    @create_resource(
        order_ns,
        create_order_model,
        order_model,
        CustomerNotFound,
        DelinquentCustomer,
        ProductNotFound,
    )
    @role_required(UserRole.DISTRIBUTOR, UserRole.SELLER)
    def post(self):
        """Create a new order"""
        current_user = ApiUtils.resolve_current_user()
        dto = {
            **order_ns.payload,
            "payment_due_date": date.fromisoformat(order_ns.payload["payment_due_date"]),
        }
        return OrderService.create(dto, current_user), HTTPStatus.CREATED

    @list_resource(order_ns, __find_all_parser, order_model)
    @role_required(UserRole.ADMIN, UserRole.DISTRIBUTOR, UserRole.SELLER)
    def get(self):
        """Get all orders"""
        current_user = ApiUtils.resolve_current_user()
        find_all_params = FindAllFactory.build_user_scoped_find_all_params(
            self.__find_all_parser,
        )
        return OrderService.find_all(find_all_params, current_user)


@order_ns.route("/<int:id>")
@order_ns.param("id", "The order identifier")
class Order(Resource):
    @get_resource(order_ns, order_model, OrderNotFound)
    @role_required(UserRole.ADMIN, UserRole.DISTRIBUTOR, UserRole.SELLER)
    def get(self, id: int):
        """Get an order by ID"""
        current_user = ApiUtils.resolve_current_user()
        return OrderService.find_first(id, current_user)

    @delete_resource(order_ns, OrderNotFound)
    @role_required(UserRole.DISTRIBUTOR, UserRole.SELLER)
    def delete(self, id: int):
        """Deactivate an order by ID"""
        current_user = ApiUtils.resolve_current_user()
        OrderService.deactivate(id, current_user)
        return "", HTTPStatus.NO_CONTENT


@order_ns.route("/<int:id>/status")
@order_ns.param("id", "The order identifier")
class OrderStatus(Resource):
    @update_resource(
        order_ns,
        update_order_status_model,
        order_model,
        OrderNotFound,
        OrderStatusTransitionInvalid,
    )
    @role_required(UserRole.DISTRIBUTOR, UserRole.SELLER)
    def patch(self, id: int):
        """Update the status of an order"""
        current_user = ApiUtils.resolve_current_user()
        return OrderService.update_status(id, order_ns.payload, current_user)
