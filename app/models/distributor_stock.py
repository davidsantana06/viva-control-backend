from sqlalchemy import DECIMAL, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column as set_mapped_column
from typing import Self

from app.extensions import db
from app.types import FindAllParams, DistributorFilter
from app.utils import ModelUtils

from .mixin.model_mixin import ModelMixin
from .mixin.timestamp_mixin import TimestampMixin


class DistributorStock(db.Model, ModelMixin, TimestampMixin):
    __tablename__ = "distributor_stocks"
    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "distributor_id",
            name="uq_distributor_stocks_product_id_distributor_id",
        ),
    )

    product_id: Mapped[int] = ModelUtils.set_foreign_key_column("products")
    distributor_id: Mapped[int] = ModelUtils.set_foreign_key_column("users")
    current_quantity: Mapped[float] = set_mapped_column(DECIMAL(15, 4), default=0)
    minimum_quantity: Mapped[float] = set_mapped_column(DECIMAL(15, 4), default=0)

    @classmethod
    def find_first_by_id(
        cls,
        id: int,
        user_filter: DistributorFilter = {},
    ) -> Self | None:
        return cls.query.filter_by(**user_filter).filter(cls.id == id).first()

    @classmethod
    def find_first_by_product_and_distributor_ids(
        cls,
        product_id: int,
        distributor_id: int,
    ) -> Self | None:
        return (
            cls.query
            .filter(cls.product_id == product_id, cls.distributor_id == distributor_id)
            .first()
        )

    @classmethod
    def find_all(
        cls,
        params: FindAllParams,
        user_filter: DistributorFilter = {}
    ) -> list[Self]:
        return (
            cls.query
            .filter_by(**user_filter)
            .order_by(cls._mount_ordering(params.sort, params.order))
            .offset(cls._calculate_offset(params.page, params.per_page))
            .limit(params.per_page)
            .all()
        )

    @classmethod
    def find_low_stock(cls, user_filter: DistributorFilter) -> list[Self]:
        return (
            cls.query
            .filter_by(**user_filter)
            .filter(cls.current_quantity <= cls.minimum_quantity)
            .all()
        )
