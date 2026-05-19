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
    CustomerNotFoundException,
    DelinquentCustomerException,
    InvalidOrderStatusTransitionException,
    OrderDeletionNotAllowedException,
    OrderNotFoundException,
    ProductNotFoundException,
)
from app.factories import FindAllFactory, UserFilterFactory
from app.services import OrderService
from app.dtos import CurrentUser
from app.types import UserRole
from app.utils import DtoUtils

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
        CustomerNotFoundException,
        DelinquentCustomerException,
        ProductNotFoundException,
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
        DtoUtils.inject_user_ids(dto, current_user)
        user_filter = UserFilterFactory.build_user_filter(current_user)
        return OrderService.create(dto, user_filter), HTTPStatus.CREATED

    @list_resource(order_ns, __find_all_parser, order_model)
    @auth_required(UserRole.ADMIN, UserRole.DISTRIBUTOR, UserRole.SELLER)
    def get(self, current_user: CurrentUser):
        """Get all orders"""
        find_all_params = FindAllFactory.build_user_scoped_find_all_params(
            self.__find_all_parser,
        )
        user_filter = UserFilterFactory.build_user_filter(
            current_user,
            find_all_params.user_scoped,
        )
        return OrderService.find_all(find_all_params, user_filter)


@order_ns.route("/<int:id>")
@order_ns.param("id", "The order identifier")
class OrderResource(Resource):
    @get_resource(order_ns, order_model, OrderNotFoundException)
    @auth_required(UserRole.ADMIN, UserRole.DISTRIBUTOR, UserRole.SELLER)
    def get(self, id: int, current_user: CurrentUser):
        """Get an order by ID"""
        user_filter = UserFilterFactory.build_user_filter(current_user)
        return OrderService.find_first_or_raise(id, user_filter)

    @delete_resource(order_ns, OrderNotFoundException, OrderDeletionNotAllowedException)
    @auth_required(UserRole.DISTRIBUTOR, UserRole.SELLER)
    def delete(self, id: int, current_user: CurrentUser):
        """Delete a cancelled order"""
        user_filter = UserFilterFactory.build_user_filter(current_user)
        OrderService.delete(id, user_filter)
        return "", HTTPStatus.NO_CONTENT


@order_ns.route("/<int:id>/status")
@order_ns.param("id", "The order identifier")
class OrderStatusResource(Resource):
    @update_resource(
        order_ns,
        update_order_status_model,
        order_model,
        OrderNotFoundException,
        InvalidOrderStatusTransitionException,
    )
    @auth_required(UserRole.DISTRIBUTOR, UserRole.SELLER)
    def patch(self, id: int, current_user: CurrentUser):
        """Update the status of an order"""
        user_filter = UserFilterFactory.build_user_filter(current_user)
        return OrderService.update_status(id, order_ns.payload, user_filter)
