from sqlalchemy import Boolean, Column
from sqlalchemy.ext.declarative import declared_attr

from .timestamp_mixin import TimestampMixin


class LifecycleMixin(TimestampMixin):
    @declared_attr
    def is_active(cls):
        return Column(Boolean, nullable=False, default=True)
