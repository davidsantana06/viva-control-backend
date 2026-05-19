from datetime import date
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
from app.exceptions import (
    CustomerNotFound,
    DelinquentCustomer,
    OrderDeletionNotAllowed,
    OrderNotFound,
    OrderStatusTransitionInvalid,
    ProductNotFound,
)
from app.factories import FindAllFactory
from app.services import OrderService
from app.types import CurrentUser, UserRole

from . import order_ns
from .models import (
    create_order_model,
    order_model,
    update_order_status_model,
)


@order_ns.route("/")
class OrderListResource(Resource):
    __find_all_parser = FindAllFactory.build_user_scoped_find_all_parser(order_ns)

    @create_resource(
        order_ns,
        create_order_model,
        order_model,
        CustomerNotFound,
        DelinquentCustomer,
        ProductNotFound,
    )
    @auth_required(UserRole.DISTRIBUTOR, UserRole.SELLER)
    def post(self, current_user: CurrentUser):
        """Create a new order"""
        dto = {
            **order_ns.payload,
            "payment_due_date": date.fromisoformat(
                order_ns.payload["payment_due_date"]
            ),
        }
        return OrderService.create(dto, current_user), HTTPStatus.CREATED

    @list_resource(order_ns, __find_all_parser, order_model)
    @auth_required(UserRole.ADMIN, UserRole.DISTRIBUTOR, UserRole.SELLER)
    def get(self, current_user: CurrentUser):
        """Get all orders"""
        find_all_params = FindAllFactory.build_user_scoped_find_all_params(
            self.__find_all_parser,
        )
        return OrderService.find_all(find_all_params, current_user)


@order_ns.route("/<int:id>")
@order_ns.param("id", "The order identifier")
class OrderResource(Resource):
    @get_resource(order_ns, order_model, OrderNotFound)
    @auth_required(UserRole.ADMIN, UserRole.DISTRIBUTOR, UserRole.SELLER)
    def get(self, id: int, current_user: CurrentUser):
        """Get an order by ID"""
        return OrderService.find_first(id, current_user)

    @delete_resource(order_ns, OrderNotFound, OrderDeletionNotAllowed)
    @auth_required(UserRole.DISTRIBUTOR, UserRole.SELLER)
    def delete(self, id: int, current_user: CurrentUser):
        """Delete a cancelled order"""
        OrderService.delete(id, current_user)
        return "", HTTPStatus.NO_CONTENT


@order_ns.route("/<int:id>/status")
@order_ns.param("id", "The order identifier")
class OrderStatusResource(Resource):
    @update_resource(
        order_ns,
        update_order_status_model,
        order_model,
        OrderNotFound,
        OrderStatusTransitionInvalid,
    )
    @auth_required(UserRole.DISTRIBUTOR, UserRole.SELLER)
    def patch(self, id: int, current_user: CurrentUser):
        """Update the status of an order"""
        return OrderService.update_status(id, order_ns.payload, current_user)
