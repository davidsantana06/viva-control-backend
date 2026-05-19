from app.dtos import CreateOrderDto, UpdateOrderStatusDto
from app.exceptions import (
    DelinquentCustomer,
    OrderDeletionNotAllowed,
    OrderNotFound,
    OrderStatusTransitionInvalid,
)
from app.extensions import db
from app.models import Order
from app.types import OrderStatus, UserFilter, UserScopedFindAllParams

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
    def create(cls, dto: CreateOrderDto, user_filter: UserFilter) -> Order:
        customer = CustomerService.find_first(dto["customer_id"], user_filter)

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
        user_filter: UserFilter,
    ) -> list[Order]:
        return Order.find_all(params, user_filter)

    @classmethod
    def find_first(cls, id: int, user_filter: UserFilter) -> Order:
        order = Order.find_first_by_id(id, user_filter)

        if not order:
            raise OrderNotFound()

        return order

    @classmethod
    def update_status(
        cls,
        id: int,
        dto: UpdateOrderStatusDto,
        user_filter: UserFilter,
    ) -> Order:
        order = cls.find_first(id, user_filter)

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
    def delete(cls, id: int, user_filter: UserFilter) -> None:
        order = cls.find_first(id, user_filter)

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
