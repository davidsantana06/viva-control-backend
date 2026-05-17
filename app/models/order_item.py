from sqlalchemy import DECIMAL
from sqlalchemy.orm import Mapped, mapped_column as set_mapped_column
from typing import Self

from app.extensions import db
from app.utils import ModelUtils

from .mixin.model_mixin import ModelMixin
from .mixin.timestamp_mixin import TimestampMixin


class OrderItem(db.Model, ModelMixin, TimestampMixin):
    __tablename__ = "order_items"

    order_id: Mapped[int] = ModelUtils.set_foreign_key_column("orders")
    product_id: Mapped[int] = ModelUtils.set_foreign_key_column("products")
    quantity: Mapped[float] = set_mapped_column(DECIMAL(15, 4))
    unit_price: Mapped[float] = set_mapped_column(DECIMAL(15, 2))
    total_price: Mapped[float] = set_mapped_column(DECIMAL(15, 2))

    @classmethod
    def find_first_by_id(cls, id: int) -> Self | None:
        return cls.query.filter(cls.id == id).first()
