from app.dtos import CreateDistributorStockDto, UpdateDistributorStockDto
from app.exceptions import DistributorStockNotFound, DistributorStockAlreadyExists
from app.models import DistributorStock
from app.types import CurrentUser, DistributorFilter, FindAllParams, UserRole


class DistributorStockService:
    @classmethod
    def create(
        cls,
        dto: CreateDistributorStockDto,
        current_user: CurrentUser,
    ) -> DistributorStock:
        dto["distributor_id"] = current_user.id

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
        user_filter = cls.__build_local_distributor_filter(current_user)
        return DistributorStock.find_all(params, user_filter)

    @classmethod
    def find_all_below_minimum(cls, current_user: CurrentUser) -> list[DistributorStock]:
        user_filter = cls.__build_local_distributor_filter(current_user)
        return DistributorStock.find_all_below_minimum(user_filter)

    @classmethod
    def find_first(cls, id: int, current_user: CurrentUser) -> DistributorStock:
        user_filter = cls.__build_local_distributor_filter(current_user)
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

    @staticmethod
    def __build_local_distributor_filter(
        current_user: CurrentUser,
    ) -> DistributorFilter:
        can_build = current_user.role in (UserRole.DISTRIBUTOR, UserRole.SELLER)
        if not can_build:
            return {}

        distributor_id = (
            current_user.id if current_user.is_distributor
            else current_user.distributor_id
        )
        return DistributorFilter(distributor_id=distributor_id)
