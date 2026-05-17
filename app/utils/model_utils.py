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
    ScopedDistributorFilter,
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

    def __build_unscoped_distributor_filter(
        current_user: CurrentUser,
    ) -> DistributorFilter:
        return DistributorFilter(distributor_id=current_user.id)

    def __build_scoped_distributor_filter(
        current_user: CurrentUser,
    ) -> ScopedDistributorFilter:
        return ScopedDistributorFilter(
            distributor_id=current_user.id,
            seller_id=None,
        )

    @classmethod
    def build_distributor_filter(
        cls,
        current_user: CurrentUser,
        user_scoped: bool = False,
    ) -> DistributorFilter | ScopedDistributorFilter:
        """
        `DISTRIBUTOR` only.

        Returns `ScopedDistributorFilter` (`seller_id=None`) when `user_scoped=True`;
        else `DistributorFilter`.
        """
        strategy = (
            cls.__build_unscoped_distributor_filter if not user_scoped
            else cls.__build_scoped_distributor_filter
        )
        return strategy[current_user]

    @staticmethod
    def build_strict_distributor_filter(
        current_user: CurrentUser,
    ) -> DistributorFilter:
        """
        `DISTRIBUTOR` or `SELLER`.
        
        Always resolves to `DistributorFilter`;
        `ADMIN` returns `{}`.
        """
        if current_user.is_admin:
            return {}

        distributor_id = (
            current_user.id if current_user.is_distributor
            else current_user.distributor_id
        )
        return DistributorFilter(distributor_id=distributor_id)

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
        """
        Any role.
        
        Dispatches to:
        - `build_distributor_filter` (`DISTRIBUTOR`);
        - `SellerFilter` (`SELLER`);
        - or `{}` (`ADMIN`).
        """
        strategies = {
            UserRole.DISTRIBUTOR: cls.build_distributor_filter,
            UserRole.SELLER: cls.__build_seller_filter,
        }
        strategy = strategies.get(current_user.role, lambda *_: {})
        return strategy(current_user, user_scoped)
