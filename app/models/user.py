from sqlalchemy import CHAR, String
from sqlalchemy.orm import (
    Mapped,
    mapped_column as set_mapped_column,
    relationship as set_relationship,
)
from typing import Self

from app.extensions import db
from app.types import DistributorFilter, FindAllParams, UserRole
from app.utils import ModelUtils

from .mixin.lifecycle_mixin import LifecycleMixin
from .mixin.model_mixin import ModelMixin


class User(db.Model, ModelMixin, LifecycleMixin):
    __tablename__ = "users"

    distributor_id: Mapped[int | None] = ModelUtils.set_foreign_key_column("users", nullable=True)
    name: Mapped[str] = set_mapped_column(String(50))
    email: Mapped[str] = set_mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = set_mapped_column(CHAR(60))
    role: Mapped[str] = set_mapped_column(String(11))

    distributor: Mapped["User | None"] = set_relationship(
        "User",
        primaryjoin="foreign(User.distributor_id) == User.id",
    )

    customers: Mapped[list["Customer"]] = set_relationship(
        "Customer",
        foreign_keys="[Customer.distributor_id]",
        back_populates="distributor",
        cascade="all, delete",
        lazy=True,
    )
    stocks: Mapped[list["DistributorStock"]] = ModelUtils.set_child_relationship("distributor")
    orders: Mapped[list["Order"]] = set_relationship(
        "Order",
        foreign_keys="[Order.distributor_id]",
        back_populates="distributor",
        cascade="all, delete",
        lazy=True,
    )

    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN
    
    @property
    def is_distributor(self) -> bool:
        return self.role == UserRole.DISTRIBUTOR

    @property
    def is_seller(self) -> bool:
        return self.role == UserRole.SELLER

    @classmethod
    def find_first_by_id(
        cls,
        id: int,
        user_filter: DistributorFilter = {}
    ) -> Self | None:
        return (
            cls.query
            .filter_by(**user_filter)
            .filter(cls.id == id, cls.is_active.is_(True))
            .first()
        )

    @classmethod
    def find_first_by_email(cls, email: str) -> Self | None:
        return cls.query.filter(cls.email == email).first()

    @classmethod
    def find_all(
        cls,
        params: FindAllParams,
        user_filter: DistributorFilter = {}
    ) -> list[Self]:
        return (
            cls.query
            .filter_by(**user_filter)
            .filter(
                cls._mount_q_filter(params.q, cls.name, cls.email),
                cls.is_active.is_(True)
            )
            .order_by(cls._mount_ordering(params.sort, params.order))
            .offset(cls._calculate_offset(params.page, params.per_page))
            .limit(params.per_page)
            .all()
        )


from .customer import Customer
from .distributor_stock import DistributorStock
from .order import Order
