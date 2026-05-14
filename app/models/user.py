from sqlalchemy import CHAR, String
from sqlalchemy.orm import (
    Mapped,
    mapped_column as set_mapped_column,
    relationship as set_relationship,
)
from typing import Self

from app.extensions import db
from app.models.mixin.lifecycle_mixin import LifecycleMixin
from app.models.mixin.model_mixin import ModelMixin
from app.types import FindAllParams
from app.utils.model_mappers import set_foreign_key_column


class User(db.Model, ModelMixin, LifecycleMixin):
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
    def find_first_by_id(cls, id: int) -> Self | None:
        return cls.query.filter(cls.id == id).first()

    @classmethod
    def find_first_by_email(cls, email: str):
        return cls.query.filter(cls.email == email).first()

    @classmethod
    def find_all(cls, params: FindAllParams) -> list[Self]:
        q_filter = cls._mount_q_filter(params.q, cls.name, cls.email)
        ordering = cls._mount_ordering(params.sort, params.order)
        offset = cls._calculate_offset(params.page, params.per_page)

        return (
            cls.query
            .filter(q_filter, cls.is_active.is_(True))
            .order_by(ordering)
            .offset(offset)
            .limit(params.per_page)
            .all()
        )
