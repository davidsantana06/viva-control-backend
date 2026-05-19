from app.dtos import CreateDistributorStockDto, UpdateDistributorStockDto
from app.exceptions import (
    DistributorStockNotFoundException,
    DistributorStockAlreadyExistsException,
)
from app.extensions import db
from app.models import DistributorStock, OrderItem
from app.types import FindAllParams, UserFilter


class DistributorStockService:
    @classmethod
    def create(
        cls,
        dto: CreateDistributorStockDto,
    ) -> DistributorStock:
        other_stock = DistributorStock.find_first_by_product_and_distributor_ids(
            dto["product_id"],
            dto["distributor_id"],
        )
        if other_stock:
            raise DistributorStockAlreadyExistsException()

        stock = DistributorStock(**dto)
        DistributorStock.save(stock)
        return stock

    @classmethod
    def find_all(
        cls,
        params: FindAllParams,
        user_filter: UserFilter,
    ) -> list[DistributorStock]:
        return DistributorStock.find_all(params, user_filter)

    @classmethod
    def find_all_below_minimum(
        cls,
        user_filter: UserFilter,
    ) -> list[DistributorStock]:
        return DistributorStock.find_all_below_minimum(user_filter)

    @staticmethod
    def find_first(id: int, user_filter: UserFilter) -> DistributorStock | None:
        return DistributorStock.find_first_by_id(id, user_filter)

    @classmethod
    def find_first_or_raise(cls, id: int, user_filter: UserFilter) -> DistributorStock:
        stock = cls.find_first(id, user_filter)

        if not stock:
            raise DistributorStockNotFoundException()

        return stock

    @classmethod
    def update(
        cls,
        id: int,
        dto: UpdateDistributorStockDto,
        user_filter: UserFilter,
    ) -> DistributorStock:
        stock = cls.find_first_or_raise(id, user_filter)
        stock.update(**dto)
        DistributorStock.save(stock)
        return stock

    @classmethod
    def delete(cls, id: int, user_filter: UserFilter) -> None:
        stock = cls.find_first_or_raise(id, user_filter)
        DistributorStock.delete(stock)

    @classmethod
    def deduct_all_staged(
        cls,
        order_items: list[OrderItem],
        distributor_id: int,
    ) -> None:
        for order_item in order_items:
            cls.__deduct_staged(order_item, distributor_id)

    @staticmethod
    def __deduct_staged(order_item: OrderItem, distributor_id: int) -> None:
        stock = DistributorStock.find_first_by_product_and_distributor_ids(
            order_item.product_id,
            distributor_id,
        )

        if not stock:
            raise DistributorStockNotFoundException()

        stock.current_quantity = max(0, stock.current_quantity - order_item.quantity)
        db.session.add(stock)

    @classmethod
    def restore_all_staged(
        cls, order_items: list[OrderItem], distributor_id: int
    ) -> None:
        for order_item in order_items:
            cls.__restore_staged(order_item, distributor_id)

    @staticmethod
    def __restore_staged(order_item: OrderItem, distributor_id: int) -> None:
        stock = DistributorStock.find_first_by_product_and_distributor_ids(
            order_item.product_id,
            distributor_id,
        )

        if not stock:
            raise DistributorStockNotFoundException()

        stock.current_quantity = stock.current_quantity + order_item.quantity
        db.session.add(stock)
