from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    MappedColumn,
    Relationship,
    mapped_column as set_mapped_column,
    relationship as set_relationship,
)

from app.types import CurrentUser, ParentFilter, RoleFilter


class ModelUtils:
    @staticmethod
    def set_primary_key_column() -> MappedColumn[int]:
        return set_mapped_column(primary_key=True, autoincrement=True)

    @staticmethod
    def set_foreign_key_column(
        table_name: str,
        nullable: bool = False,
    ) -> MappedColumn[int]:
        related_id = ForeignKey(f"{table_name}.id")
        return set_mapped_column(related_id, nullable=nullable)

    @staticmethod
    def set_child_relationship(back_populates: str) -> Relationship[list]:
        return set_relationship(
            back_populates=back_populates,
            cascade="all, delete",
            lazy=True,
        )

    @staticmethod
    def set_parent_relationship(back_populates: str) -> Relationship:
        return set_relationship(back_populates=back_populates)

    @classmethod
    def build_parent_filter(cls, current_user: CurrentUser) -> ParentFilter:
        if not current_user.is_distributor:
            return {}

        return {"parent_id": current_user.id}

    @classmethod
    def build_role_filter(cls, current_user: CurrentUser) -> RoleFilter:
        can_filter = current_user.is_distributor or current_user.is_seller
        if not can_filter:
            return {}

        column = f"{current_user.role.lower()}_id"
        return {column: current_user.id}
