from app.dtos import CreateCustomerDto, UpdateCustomerDto
from app.exceptions import CustomerNotFoundException
from app.models import Customer
from app.types import UserFilter, UserScopedFindAllParams


class CustomerService:
    @staticmethod
    def create(dto: CreateCustomerDto) -> Customer:
        customer = Customer(**dto)
        Customer.save(customer)
        return customer

    @staticmethod
    def find_all(
        params: UserScopedFindAllParams,
        user_filter: UserFilter,
    ) -> list[Customer]:
        return Customer.find_all(params, user_filter)

    @staticmethod
    def find_first(id: int, user_filter: UserFilter) -> Customer | None:
        return Customer.find_first_by_id(id, user_filter)

    @classmethod
    def find_first_or_raise(cls, id: int, user_filter: UserFilter) -> Customer:
        customer = cls.find_first(id, user_filter)

        if not customer:
            raise CustomerNotFoundException()

        return customer

    @classmethod
    def update(
        cls,
        id: int,
        dto: UpdateCustomerDto,
        user_filter: UserFilter,
    ) -> Customer:
        customer = cls.find_first_or_raise(id, user_filter)
        customer.update(**dto)
        Customer.save(customer)
        return customer

    @classmethod
    def delete(cls, id: int, user_filter: UserFilter) -> None:
        customer = cls.find_first_or_raise(id, user_filter)
        Customer.delete(customer)
