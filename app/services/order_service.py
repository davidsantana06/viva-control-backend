from app.dtos import CreateOrderDto, CreateOrderItemDto, UpdateOrderStatusDto
from app.exceptions import (
    CustomerNotFound,
    CustomerPaymentOverdue,
    OrderNotFound,
    OrderStatusTransitionInvalid,
    ProductNotFound,
)
from app.extensions import db
from app.factories import UserFilterFactory
from app.models import Customer, DistributorStock, Order, OrderItem, Product
from app.types import CurrentUser, OrderStatus, UserScopedFindAllParams
from app.utils import DtoUtils


class OrderService:
    __VALID_STATUS_TRANSITIONS: dict[OrderStatus, set[OrderStatus]] = {
        OrderStatus.PENDING: {
            OrderStatus.CANCELLED,
            OrderStatus.DELIVERED_UNPAID,
            OrderStatus.DELIVERED_PAID,
        },
        OrderStatus.DELIVERED_UNPAID: {OrderStatus.DELIVERED_PAID},
        OrderStatus.CANCELLED: set(),
        OrderStatus.DELIVERED_PAID: set(),
    }

    @classmethod
    def create(cls, dto: CreateOrderDto, current_user: CurrentUser) -> Order:
        DtoUtils.inject_user_ids(dto, current_user)
        user_filter = UserFilterFactory.build_user_filter(current_user)

        customer = Customer.find_first_by_id(dto["customer_id"], user_filter)
        if not customer:
            raise CustomerNotFound()

        overdue_order = Order.find_first_overdue_by_customer_id(customer.id)
        if overdue_order:
            raise CustomerPaymentOverdue()

        items, stock_updates, total_amount = cls.__prepare_items(
            dto["items"],
            dto["distributor_id"],
        )
        net_amount = cls.__calculate_net_amount(
            total_amount,
            dto["discount_pct"],
        )

        order = Order(
            customer_id=dto["customer_id"],
            distributor_id=dto["distributor_id"],
            seller_id=dto.get("seller_id"),
            payment_method_id=dto.get("payment_method_id"),
            total_amount=total_amount,
            discount_pct=dto["discount_pct"],
            net_amount=net_amount,
            payment_installments=dto["payment_installments"],
            payment_due_date=dto["payment_due_date"],
            notes=dto.get("notes"),
            status=OrderStatus.PENDING,
        )
        order.items = items
        db.session.add(order)

        for stock, quantity in stock_updates:
            stock.current_quantity = max(0, stock.current_quantity - quantity)
            db.session.add(stock)

        db.session.commit()
        return order

    @staticmethod
    def __calculate_net_amount(total_amount: float, discount_pct: float) -> float:
        return round(total_amount * (1 - discount_pct / 100), 2)

    @staticmethod
    def find_all(
        params: UserScopedFindAllParams,
        current_user: CurrentUser,
    ) -> list[Order]:
        user_filter = UserFilterFactory.build_user_filter(
            current_user, params.user_scoped
        )
        return Order.find_all(params, user_filter)

    @staticmethod
    def find_first(id: int, current_user: CurrentUser) -> Order:
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
        user_filter = UserFilterFactory.build_user_filter(current_user)

        order = Order.find_first_by_id(id, user_filter)
        if not order:
            raise OrderNotFound()

        current_status = OrderStatus(order.status)
        new_status = OrderStatus(dto["status"])

        if new_status not in cls.__VALID_STATUS_TRANSITIONS[current_status]:
            raise OrderStatusTransitionInvalid()

        if new_status == OrderStatus.CANCELLED:
            for item in order.items:
                stock = DistributorStock.find_first_by_product_and_distributor_ids(
                    item.product_id,
                    order.distributor_id,
                )
                if stock:
                    stock.current_quantity = stock.current_quantity + item.quantity
                    db.session.add(stock)

        order.status = new_status
        db.session.add(order)
        db.session.commit()
        return order

    @classmethod
    def deactivate(cls, id: int, current_user: CurrentUser) -> None:
        # user_scoped=True: DISTRIBUTOR only deactivates own orders (seller_id=NULL)
        user_filter = UserFilterFactory.build_user_filter(
            current_user, user_scoped=True
        )
        order = Order.find_first_by_id(id, user_filter)
        if not order:
            raise OrderNotFound()
        Order.deactivate(order)
        Order.save(order)

    @staticmethod
    def __prepare_items(
        items_dto: list,
        distributor_id: int,
    ) -> tuple[list[OrderItem], list, float]:
        stock_updates = []
        items = []
        total_amount = 0.0

        for item_dto in items_dto:
            product_id = item_dto["product_id"]
            quantity = item_dto["quantity"]

            product = Product.find_first_by_id(product_id)
            if not product:
                raise ProductNotFound()

            stock = DistributorStock.find_first_by_product_and_distributor_ids(
                product_id,
                distributor_id
            )
            if stock:
                stock_updates.append((stock, quantity))

            raw_price = item_dto.get("unit_price")
            unit_price = raw_price if raw_price is not None else product.suggested_price
            total_price = round(quantity * unit_price, 2)
            total_amount += total_price

            items.append(
                OrderItem(
                    product_id=product_id,
                    quantity=quantity,
                    unit_price=unit_price,
                    total_price=total_price,
                )
            )

        return items, stock_updates, round(total_amount, 2)
