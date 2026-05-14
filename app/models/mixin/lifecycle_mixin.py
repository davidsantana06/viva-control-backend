from sqlalchemy import Boolean, Column
from sqlalchemy.ext.declarative import declared_attr
from typing import Self

from app.extensions import db
from .timestamp_mixin import TimestampMixin


class LifecycleMixin(TimestampMixin):
    @declared_attr
    def is_active(cls):
        return Column(Boolean, nullable=False, default=True)

    @classmethod
    def deactivate(cls, model: Self) -> None:
        model.is_active = False
        db.session.add(model)
        db.session.commit()
