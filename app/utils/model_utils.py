from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    MappedColumn,
    Relationship,
    mapped_column as set_mapped_column,
    relationship as set_relationship,
)

from app.types import (
    CurrentUser,
    DistributorFilter,
    DistributorOnlyFilter,
    SellerFilter,
    UserFilter,
    UserRole,
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
        return set_relationship(back_populates=back_populates)

    @staticmethod
    def build_distributor_filter(
        current_user: CurrentUser,
        user_scoped: bool = False,
    ) -> DistributorFilter | DistributorOnlyFilter:
        user_filter = {"distributor_id": current_user.id}
        if user_scoped:
            user_filter["seller_id"] = None
        return user_filter

    @staticmethod
    def __build_seller_filter(
        current_user: CurrentUser,
        _: bool = False,
    ) -> SellerFilter:
        return SellerFilter(seller_id=current_user.id)

    @classmethod
    def build_user_filter(
        cls,
        current_user: CurrentUser,
        user_scoped: bool = False,
    ) -> UserFilter:
        strategies = {
            UserRole.DISTRIBUTOR: cls.build_distributor_filter,
            UserRole.SELLER: cls.__build_seller_filter,
        }
        strategy = strategies.get(current_user.role, lambda *_: {})
        return strategy(current_user, user_scoped)
