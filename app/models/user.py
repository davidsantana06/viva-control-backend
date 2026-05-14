from sqlalchemy import CHAR, String
from sqlalchemy.orm import (
    Mapped,
    mapped_column as set_mapped_column,
    relationship as set_relationship,
)
from typing import Self

from app.extensions import db
from app.models.contract.user_repository import UserRepository
from app.models.mixin.lifecycle_mixin import LifecycleMixin
from app.models.mixin.model_mixin import ModelMixin
from app.types import SortOrder
from app.utils.model_mappers import set_foreign_key_column


class User(db.Model, ModelMixin, LifecycleMixin, UserRepository):
    __tablename__ = "users"

    parent_id: Mapped[int | None] = set_foreign_key_column("users", nullable=True)
    name: Mapped[str] = set_mapped_column(String(50))
    email: Mapped[str] = set_mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = set_mapped_column(CHAR(60))
    role: Mapped[str] = set_mapped_column(String(11))

    parent: Mapped["User | None"] = set_relationship(
        "User",
        primaryjoin="foreign(User.parent_id) == User.id",
    )

    @classmethod
    def find_first(cls, id: int) -> Self | None:
        return cls.query.filter(cls.id == id).first()

    @classmethod
    def find_all(
        cls,
        q: str | None = None,
        order: SortOrder = "ASC",
        sort: str = "id",
        page: int = 1,
        per_page: int = 10,
    ) -> list[Self]:
        ordering = cls._mount_ordering(sort, order)
        q_filter = cls._mount_q_filter(q, cls.name, cls.email)

        return (
            cls.query
            .filter(q_filter, cls.is_active.is_(True))
            .order_by(ordering)
            .offset(cls._calculate_offset(page, per_page))
            .limit(per_page)
            .all()
        )
