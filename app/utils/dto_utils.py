from app.types import CurrentUser, UserRole


class DtoUtils:
    @staticmethod
    def __inject_distributor_id(dto: dict, current_user: CurrentUser) -> None:
        dto["distributor_id"] = current_user.id

    @staticmethod
    def __inject_distributor_and_seller_id(
        dto: dict,
        current_user: CurrentUser,
    ) -> None:
        dto["seller_id"] = current_user.id
        dto["distributor_id"] = current_user.parent_id

    @classmethod
    def inject_distributor_and_or_seller_ids(
        cls,
        dto: dict,
        current_user: CurrentUser,
    ) -> None:
        strategies = {
            UserRole.DISTRIBUTOR: cls.__inject_distributor_id,
            UserRole.SELLER: cls.__inject_distributor_and_seller_id,
        }
        strategy = strategies[current_user.role]
        strategy(dto, current_user)
