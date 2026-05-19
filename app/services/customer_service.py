from app.dtos import CreateCustomerDto, UpdateCustomerDto
from app.exceptions import CustomerNotFound
from app.factories import UserFilterFactory
from app.models import Customer
from app.types import CurrentUser, UserScopedFindAllParams
from app.utils import DtoUtils


class CustomerService:
    @staticmethod
    def create(dto: CreateCustomerDto, current_user: CurrentUser) -> Customer:
        DtoUtils.inject_user_ids(dto, current_user)
        customer = Customer(**dto)
        Customer.save(customer)
        return customer

    @staticmethod
    def find_all(
        params: UserScopedFindAllParams,
        current_user: CurrentUser,
    ) -> list[Customer]:
        user_filter = UserFilterFactory.build_user_filter(
            current_user,
            params.user_scoped,
        )
        return Customer.find_all(params, user_filter)

    @staticmethod
    def find_first(id: int, current_user: CurrentUser) -> Customer:
        user_filter = UserFilterFactory.build_user_filter(current_user)
        customer = Customer.find_first_by_id(id, user_filter)

        if not customer:
            raise CustomerNotFound()

        return customer

    @classmethod
    def update(
        cls,
        id: int,
        dto: UpdateCustomerDto,
        current_user: CurrentUser,
    ) -> Customer:
        customer = cls.find_first(id, current_user)
        customer.update(**dto)
        Customer.save(customer)
        return customer

    @classmethod
    def delete(cls, id: int, current_user: CurrentUser) -> None:
        customer = cls.find_first(id, current_user)
        Customer.delete(customer)
