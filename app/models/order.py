from datetime import date
from sqlalchemy import Date, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column as set_mapped_column
from typing import Self

from app.extensions import db
from app.types import FindAllParams, OrderStatus, UserFilter
from app.utils import ModelUtils

from .mixin.lifecycle_mixin import LifecycleMixin
from .mixin.model_mixin import ModelMixin


class Order(db.Model, ModelMixin, LifecycleMixin):
    __tablename__ = "orders"

    customer_id: Mapped[int] = ModelUtils.set_foreign_key_column("customers")
    distributor_id: Mapped[int] = ModelUtils.set_foreign_key_column("users")
    seller_id: Mapped[int | None] = ModelUtils.set_foreign_key_column("users", nullable=True)
    payment_method_id: Mapped[int | None] = ModelUtils.set_foreign_key_column("payment_methods", nullable=True)
    discount_pct: Mapped[int] = set_mapped_column(Integer, default=0)
    payment_installments: Mapped[int] = set_mapped_column(Integer, default=1)
    payment_due_date: Mapped[date] = set_mapped_column(Date)
    notes: Mapped[str | None] = set_mapped_column(Text, nullable=True)
    status: Mapped[str] = set_mapped_column(String(16), default=OrderStatus.PENDING)

    items: Mapped[list["OrderItem"]] = ModelUtils.set_child_relationship("order")

    @property
    def is_pending(self) -> bool:
        return self.status == OrderStatus.PENDING
    
    @property
    def is_delivered_unpaid(self) -> bool:
        return self.status == OrderStatus.DELIVERED_UNPAID
    
    @property
    def is_delivered_paid(self) -> bool:
        return self.status == OrderStatus.DELIVERED_PAID
    
    @property
    def is_cancelled(self) -> bool:
        return self.status == OrderStatus.CANCELLED

    @property
    def total_amount(self) -> float:
        return sum(item.total_price for item in self.items) or 0.0

    @property
    def discount_amount(self) -> float:
        fraction = self.discount_pct / 100
        return self.total_amount * fraction

    @property
    def net_amount(self) -> float:
        return self.total_amount - self.discount_amount

    @classmethod
    def find_first_by_id(cls, id: int, user_filter: UserFilter = {}) -> Self | None:
        return (
            cls.query
            .filter_by(**user_filter)
            .filter(cls.id == id, cls.is_active.is_(True))
            .first()
        )

    @classmethod
    def find_first_delivered_unpaid_by_customer_id(cls, customer_id: int) -> Self | None:
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


from .order_item import OrderItem
