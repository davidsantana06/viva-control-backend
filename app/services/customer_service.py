from app.dtos import CreateCustomerDto, UpdateCustomerDto
from app.exceptions import CustomerNotFound
from app.models import Customer, User
from app.types import CurrentUser, FindAllParams, UserRole
from app.utils import ModelUtils


class CustomerService:
    @staticmethod
    def create(dto: CreateCustomerDto, current_user: CurrentUser) -> Customer:
        if current_user.role == UserRole.SELLER:
            seller = User.find_first_by_id(current_user.id)
            dto["seller_id"] = current_user.id
            dto["distributor_id"] = seller.parent_id
        elif current_user.role == UserRole.DISTRIBUTOR:
            dto["distributor_id"] = current_user.id

        customer = Customer(**dto)
        Customer.save(customer)
        return customer

    @staticmethod
    def find_all(params: FindAllParams, current_user: CurrentUser) -> list[Customer]:
        role_filter = ModelUtils.build_role_filter(current_user)
        return Customer.find_all(params, role_filter)

    @staticmethod
    def find_first(id: int, current_user: CurrentUser) -> Customer:
        role_filter = ModelUtils.build_role_filter(current_user)
        customer = Customer.find_first_by_id(id, role_filter)

        if not customer:
            raise CustomerNotFound()

        return customer

    @classmethod
    def update(cls, id: int, dto: UpdateCustomerDto, current_user: CurrentUser) -> Customer:
        customer = cls.find_first(id, current_user)
        customer.update(**dto)
        Customer.save(customer)
        return customer

    @classmethod
    def deactivate(cls, id: int, current_user: CurrentUser) -> None:
        customer = cls.find_first(id, current_user)
        Customer.deactivate(customer)
        Customer.save(customer)
