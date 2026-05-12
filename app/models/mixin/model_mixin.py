from flask_sqlalchemy.model import Model
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped

from app.extensions import db
from app.utils.model_mappers import set_primary_key_column
from .timestamp_mixin import TimestampMixin


class ModelMixin(TimestampMixin):
    @declared_attr
    def id(cls) -> Mapped[int]:
        return set_primary_key_column()

    @staticmethod
    def save(model: Model) -> None:
        db.session.add(model)
        db.session.commit()

    @staticmethod
    def delete(model: Model) -> None:
        db.session.delete(model)
        db.session.commit()
