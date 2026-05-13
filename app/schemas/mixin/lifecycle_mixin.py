from flask_restx.fields import Boolean
from .timestamp_mixin import TimestampMixin, timestamp_mixin


class LifecycleMixin(TimestampMixin):
    is_active: bool


lifecycle_mixin = LifecycleMixin(
    is_active=Boolean(title="Is active", readonly=True),
    **timestamp_mixin,
)
