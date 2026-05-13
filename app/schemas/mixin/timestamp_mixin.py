from datetime import datetime
from flask_restx.fields import DateTime
from typing import TypedDict


class TimestampMixin(TypedDict):
    created_at: datetime
    updated_at: datetime


timestamp_mixin = TimestampMixin(
    created_at=DateTime(title="Created at", readonly=True),
    updated_at=DateTime(title="Updated at", readonly=True),
)
