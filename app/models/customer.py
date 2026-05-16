from datetime import date
from sqlalchemy import Date, String, Text
from sqlalchemy.orm import Mapped, mapped_column as set_mapped_column
from typing import Self

from app.extensions import db
from app.types import FindAllParams, UserFilter
from app.utils import ModelUtils

from .mixin.lifecycle_mixin import LifecycleMixin
from .mixin.model_mixin import ModelMixin


class Customer(db.Model, ModelMixin, LifecycleMixin):
    __tablename__ = "customers"

    distributor_id: Mapped[int] = ModelUtils.set_foreign_key_column("users")
    seller_id: Mapped[int | None] = ModelUtils.set_foreign_key_column("users", nullable=True)
    name: Mapped[str] = set_mapped_column(String(50))
    document: Mapped[str] = set_mapped_column(String(14))
    document_type: Mapped[str] = set_mapped_column(String(4))
    phone: Mapped[str | None] = set_mapped_column(String(14), nullable=True)
    address: Mapped[str | None] = set_mapped_column(Text, nullable=True)
    birth_date: Mapped[date | None] = set_mapped_column(Date, nullable=True)
    notes: Mapped[str | None] = set_mapped_column(Text, nullable=True)

    @classmethod
    def find_first_by_id(cls, id: int, user_filter: UserFilter = {}) -> Self | None:
        return (
            cls.query
            .filter_by(**user_filter)
            .filter(cls.id == id, cls.is_active.is_(True))
            .first()
        )

    @classmethod
    def find_all(cls, params: FindAllParams, user_filter: UserFilter = {}) -> list[Self]:
        return (
            cls.query
            .filter_by(**user_filter)
            .filter(
                cls._mount_q_filter(params.q, cls.name, cls.document),
                cls.is_active.is_(True)
            )
            .order_by(cls._mount_ordering(params.sort, params.order))
            .offset(offset = cls._calculate_offset(params.page, params.per_page))
            .limit(params.per_page)
            .all()
        )
