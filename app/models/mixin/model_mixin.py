from flask_sqlalchemy.model import Model
from sqlalchemy import ColumnElement, asc, desc, or_, true
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped
from typing import Self

from app.extensions import db
from app.types import Filter, Ordering, SortOrder
from app.utils import ModelUtils


class ModelMixin(Model):
    @declared_attr
    def id(cls) -> Mapped[int]:
        return ModelUtils.set_primary_key_column()

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def save(model: Self) -> None:
        db.session.add(model)
        db.session.commit()

    @classmethod
    def _mount_q_filter(cls, q: str | None, *columns: ColumnElement) -> Filter:
        if not q:
            return true()

        return or_(*[column.icontains(q) for column in columns])

    @classmethod
    def _mount_ordering(cls, sort: str, order: SortOrder) -> Ordering:
        sort_column = getattr(cls, sort, cls.id)
        is_ascending = order == "ASC"
        return asc(sort_column) if is_ascending else desc(sort_column)

    @staticmethod
    def _calculate_offset(page: int, per_page: int) -> int:
        return (page - 1) * per_page
