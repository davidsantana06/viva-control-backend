from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column as set_mapped_column
from typing import Self

from app.extensions import db
from app.models.mixin.lifecycle_mixin import LifecycleMixin
from app.models.mixin.model_mixin import ModelMixin
from app.types import FindAllParams


class PaymentMethod(db.Model, ModelMixin, LifecycleMixin):
    __tablename__ = "payment_methods"

    name: Mapped[str] = set_mapped_column(String(50))

    @classmethod
    def find_first_by_id(cls, id: int) -> Self | None:
        return cls.query.filter(cls.id == id, cls.is_active.is_(True)).first()

    @classmethod
    def find_all(cls, params: FindAllParams) -> list[Self]:
        return (
            cls.query
            .filter(
                cls._mount_q_filter(params.q, cls.name),
                cls.is_active.is_(True)
            )
            .order_by(cls._mount_ordering(params.sort, params.order))
            .offset(cls._calculate_offset(params.page, params.per_page))
            .limit(params.per_page)
            .all()
        )
