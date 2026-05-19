from app.dtos import CreateOrderDto, UpdateOrderStatusDto
from app.exceptions import (
    DelinquentCustomer,
    OrderDeletionNotAllowed,
    OrderNotFound,
    OrderStatusTransitionInvalid,
)
from app.extensions import db
from app.factories import UserFilterFactory
from app.models import Order
from app.types import CurrentUser, OrderStatus, UserScopedFindAllParams
from app.utils import DtoUtils

from .customer_service import CustomerService
from .distributor_stock_service import DistributorStockService
from .order_item_service import OrderItemService


class OrderService:
    __VALID_STATUS_TRANSITIONS = {
        OrderStatus.PENDING: {
            OrderStatus.CANCELLED,
            OrderStatus.DELIVERED_UNPAID,
            OrderStatus.DELIVERED_PAID,
        },
        OrderStatus.DELIVERED_UNPAID: {OrderStatus.DELIVERED_PAID},
        OrderStatus.DELIVERED_PAID: set(),
        OrderStatus.CANCELLED: set(),
    }

    @classmethod
    def create(cls, dto: CreateOrderDto, current_user: CurrentUser) -> Order:
        DtoUtils.inject_user_ids(dto, current_user)
        customer = CustomerService.find_first(dto["customer_id"], current_user)

        du_order = Order.find_first_delivered_unpaid_by_customer_id(customer.id)
        if du_order:
            raise DelinquentCustomer()

        order_items = OrderItemService.create_all_staged(dto.pop("items"))
        order = Order(**dto)
        order.items = order_items
        db.session.add(order)
        DistributorStockService.deduct_all_staged(order_items, order.distributor_id)
        db.session.commit()
        return order

    @staticmethod
    def find_all(
        params: UserScopedFindAllParams,
        current_user: CurrentUser,
    ) -> list[Order]:
        user_filter = UserFilterFactory.build_user_filter(
            current_user,
            params.user_scoped,
        )
        return Order.find_all(params, user_filter)

    @classmethod
    def find_first(cls, id: int, current_user: CurrentUser) -> Order:
        user_filter = UserFilterFactory.build_user_filter(current_user)
        order = Order.find_first_by_id(id, user_filter)

        if not order:
            raise OrderNotFound()

        return order

    @classmethod
    def update_status(
        cls,
        id: int,
        dto: UpdateOrderStatusDto,
        current_user: CurrentUser,
    ) -> Order:
        order = cls.find_first(id, current_user)

        current_status = OrderStatus(order.status)
        new_status = OrderStatus(dto["status"])
        cls.__validate_status_transition(current_status, new_status)
        order.status = new_status

        if order.is_cancelled:
            DistributorStockService.restore_all_staged(
                order.items,
                order.distributor_id,
            )

        db.session.add(order)
        db.session.commit()
        return order

    @classmethod
    def delete(cls, id: int, current_user: CurrentUser) -> None:
        order = cls.find_first(id, current_user)

        if not order.is_cancelled:
            raise OrderDeletionNotAllowed()

        Order.delete(order)

    @classmethod
    def __validate_status_transition(
        cls,
        current: OrderStatus,
        new: OrderStatus,
    ) -> None:
        if new not in cls.__VALID_STATUS_TRANSITIONS[current]:
            raise OrderStatusTransitionInvalid()
