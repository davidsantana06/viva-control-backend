from sqlalchemy import DECIMAL, String, Text
from sqlalchemy.orm import Mapped, mapped_column as set_mapped_column
from typing import Self

from app.extensions import db
from app.types import FindAllParams
from app.utils import ModelUtils

from .mixin.lifecycle_mixin import LifecycleMixin
from .mixin.model_mixin import ModelMixin


class Product(db.Model, ModelMixin, LifecycleMixin):
    __tablename__ = "products"

    name: Mapped[str] = set_mapped_column(String(100))
    sku: Mapped[str] = set_mapped_column(String(50), unique=True)
    description: Mapped[str | None] = set_mapped_column(Text, nullable=True)
    suggested_price: Mapped[float] = set_mapped_column(DECIMAL(15, 2))

    order_items: Mapped[list["OrderItem"]] = ModelUtils.set_child_relationship("product")

    @classmethod
    def find_first_by_id(cls, id: int) -> Self | None:
        return cls.query.filter(cls.id == id, cls.is_active.is_(True)).first()

    @classmethod
    def find_first_by_sku(cls, sku: str) -> Self | None:
        return cls.query.filter(cls.sku == sku).first()

    @classmethod
    def find_all(cls, params: FindAllParams) -> list[Self]:
        return (
            cls.query.filter(
                cls._mount_q_filter(params.q, cls.name, cls.sku),
                cls.is_active.is_(True),
            )
            .order_by(cls._mount_ordering(params.sort, params.order))
            .offset(offset=cls._calculate_offset(params.page, params.per_page))
            .limit(params.per_page)
            .all()
        )


from .order_item import OrderItem
