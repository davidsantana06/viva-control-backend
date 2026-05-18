from app.dtos import CreateDistributorStockDto, UpdateDistributorStockDto
from app.exceptions import DistributorStockNotFound, DistributorStockAlreadyExists
from app.extensions import db
from app.factories import UserFilterFactory
from app.models import DistributorStock, OrderItem
from app.types import CurrentUser, FindAllParams
from app.utils import DtoUtils


class DistributorStockService:
    @classmethod
    def create(
        cls,
        dto: CreateDistributorStockDto,
        current_user: CurrentUser,
    ) -> DistributorStock:
        DtoUtils.inject_user_ids(dto, current_user)

        other_stock = DistributorStock.find_first_by_product_and_distributor_ids(
            dto["product_id"],
            dto["distributor_id"],
        )
        if other_stock:
            raise DistributorStockAlreadyExists()

        stock = DistributorStock(**dto)
        DistributorStock.save(stock)
        return stock

    @classmethod
    def find_all(
        cls,
        params: FindAllParams,
        current_user: CurrentUser,
    ) -> list[DistributorStock]:
        user_filter = UserFilterFactory.build_strict_distributor_filter(current_user)
        return DistributorStock.find_all(params, user_filter)

    @classmethod
    def find_all_below_minimum(
        cls,
        current_user: CurrentUser,
    ) -> list[DistributorStock]:
        user_filter = UserFilterFactory.build_strict_distributor_filter(current_user)
        return DistributorStock.find_all_below_minimum(user_filter)

    @classmethod
    def find_first(cls, id: int, current_user: CurrentUser) -> DistributorStock:
        user_filter = UserFilterFactory.build_strict_distributor_filter(current_user)
        stock = DistributorStock.find_first_by_id(id, user_filter)

        if not stock:
            raise DistributorStockNotFound()

        return stock

    @classmethod
    def update(
        cls,
        id: int,
        dto: UpdateDistributorStockDto,
        current_user: CurrentUser,
    ) -> DistributorStock:
        stock = cls.find_first(id, current_user)
        stock.update(**dto)
        DistributorStock.save(stock)
        return stock

    @classmethod
    def delete(cls, id: int, current_user: CurrentUser) -> None:
        stock = cls.find_first(id, current_user)
        DistributorStock.delete(stock)

    @classmethod
    def deduct_all_staged(cls, order_items: list[OrderItem], distributor_id: int) -> None:
        for order_item in order_items:
            cls.__deduct_staged(order_item, distributor_id)

    @staticmethod
    def __deduct_staged(order_item: OrderItem, distributor_id: int) -> None:
        stock = DistributorStock.find_first_by_product_and_distributor_ids(
            order_item.product_id,
            distributor_id,
        )

        if not stock:
            raise DistributorStockNotFound()

        stock.current_quantity = max(0, stock.current_quantity - order_item.quantity)
        db.session.add(stock)

    @classmethod
    def restore_all_staged(cls, order_items: list[OrderItem], distributor_id: int) -> None:
        for order_item in order_items:
            cls.__restore_staged(order_item, distributor_id)

    @staticmethod
    def __restore_staged(order_item: OrderItem, distributor_id: int) -> None:
        stock = DistributorStock.find_first_by_product_and_distributor_ids(
            order_item.product_id,
            distributor_id,
        )

        if not stock:
            raise DistributorStockNotFound()

        stock.current_quantity = stock.current_quantity + order_item.quantity
        db.session.add(stock)
