from datetime import date
from sqlalchemy import DECIMAL, Date, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column as set_mapped_column, relationship
from typing import Self

from app.extensions import db
from app.types import FindAllParams, OrderStatus, UserFilter
from app.utils import ModelUtils

from .mixin.lifecycle_mixin import LifecycleMixin
from .mixin.model_mixin import ModelMixin
from .order_item import OrderItem


class Order(db.Model, ModelMixin, LifecycleMixin):
    __tablename__ = "orders"

    customer_id: Mapped[int] = ModelUtils.set_foreign_key_column("customers")
    distributor_id: Mapped[int] = ModelUtils.set_foreign_key_column("users")
    seller_id: Mapped[int | None] = ModelUtils.set_foreign_key_column("users", nullable=True)
    payment_method_id: Mapped[int | None] = ModelUtils.set_foreign_key_column("payment_methods", nullable=True)
    total_amount: Mapped[float] = set_mapped_column(DECIMAL(15, 2))
    discount_pct: Mapped[float] = set_mapped_column(DECIMAL(5, 2), default=0)
    net_amount: Mapped[float] = set_mapped_column(DECIMAL(15, 2))
    payment_installments: Mapped[int] = set_mapped_column(Integer, default=1)
    payment_due_date: Mapped[date] = set_mapped_column(Date)
    notes: Mapped[str | None] = set_mapped_column(Text, nullable=True)
    status: Mapped[str] = set_mapped_column(String(16), default=OrderStatus.PENDING)

    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        cascade="all, delete-orphan",
        lazy=True,
        foreign_keys="[OrderItem.order_id]",
    )

    @classmethod
    def find_first_by_id(cls, id: int, user_filter: UserFilter = {}) -> Self | None:
        return (
            cls.query
            .filter_by(**user_filter)
            .filter(cls.id == id, cls.is_active.is_(True))
            .first()
        )

    @classmethod
    def find_first_overdue_by_customer_id(cls, customer_id: int) -> Self | None:
        return (
            cls.query
            .filter(
                cls.customer_id == customer_id,
                cls.status == OrderStatus.DELIVERED_UNPAID,
                cls.payment_due_date < date.today(),
                cls.is_active.is_(True),
            )
            .first()
        )

    @classmethod
    def find_all(cls, params: FindAllParams, user_filter: UserFilter = {}) -> list[Self]:
        return (
            cls.query
            .filter_by(**user_filter)
            .filter(
                cls._mount_q_filter(params.q, cls.notes),
                cls.is_active.is_(True),
            )
            .order_by(cls._mount_ordering(params.sort, params.order))
            .offset(cls._calculate_offset(params.page, params.per_page))
            .limit(params.per_page)
            .all()
        )
