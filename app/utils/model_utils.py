from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    MappedColumn,
    Relationship,
    mapped_column as set_mapped_column,
    relationship as set_relationship,
)


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
        return set_relationship(back_populates=back_populates, lazy=True)
