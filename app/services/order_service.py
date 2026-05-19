from app.dtos import CreateOrderDto, UpdateOrderStatusDto
from app.exceptions import (
    DelinquentCustomerException,
    InvalidOrderStatusTransitionException,
    OrderDeletionNotAllowedException,
    OrderNotFoundException,
)
from app.extensions import db
from app.models import Order
from app.dtos import UserScopedFindAllParams
from app.types import OrderStatus, UserFilter

from .customer_service import CustomerService
from .distributor_stock_service import DistributorStockService
from .order_item_service import OrderItemService


class OrderService:
    @classmethod
    def create(cls, dto: CreateOrderDto, user_filter: UserFilter) -> Order:
        customer = CustomerService.find_first_or_raise(dto["customer_id"], user_filter)

        du_order = Order.find_first_delivered_unpaid_by_customer_id(customer.id)
        if du_order:
            raise DelinquentCustomerException()

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

    @staticmethod
    def find_first(id: int, user_filter: UserFilter) -> Order | None:
        return Order.find_first_by_id(id, user_filter)

    @classmethod
    def find_first_or_raise(cls, id: int, user_filter: UserFilter) -> Order:
        order = cls.find_first(id, user_filter)

        if not order:
            raise OrderNotFoundException()

        return order

    @classmethod
    def update_status(
        cls,
        id: int,
        dto: UpdateOrderStatusDto,
        user_filter: UserFilter,
    ) -> Order:
        order = cls.find_first_or_raise(id, user_filter)
        new_status = OrderStatus(dto["status"])

        if not order.can_transition_to(new_status):
            raise InvalidOrderStatusTransitionException()

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
        order = cls.find_first_or_raise(id, user_filter)

        if not order.is_cancelled:
            raise OrderDeletionNotAllowedException()

        Order.delete(order)
