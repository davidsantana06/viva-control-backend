from flask_restx import Resource
from http import HTTPStatus

from app.decorators import (
    create_resource,
    deactivate_resource,
    get_resource,
    list_resource,
    role_required,
    update_resource,
)
from app.exceptions import CustomerNotFound
from app.services import CustomerService
from app.types import UserRole
from app.utils import ApiUtils

from . import customer_ns
from .models import create_customer_model, customer_model, update_customer_model


@customer_ns.route("/")
class CustomerList(Resource):
    __find_all_parser = ApiUtils.build_find_all_parser(customer_ns)

    @create_resource(customer_ns, create_customer_model, customer_model)
    @role_required(UserRole.ADMIN, UserRole.DISTRIBUTOR, UserRole.SELLER)
    def post(self):
        """Create a new customer"""
        current_user = ApiUtils.resolve_current_user()
        return CustomerService.create(customer_ns.payload, current_user), HTTPStatus.CREATED

    @list_resource(customer_ns, __find_all_parser, customer_model)
    @role_required(UserRole.ADMIN, UserRole.DISTRIBUTOR, UserRole.SELLER)
    def get(self):
        """Get all customers"""
        current_user = ApiUtils.resolve_current_user()
        find_all_params = ApiUtils.build_find_all_params(self.__find_all_parser)
        return CustomerService.find_all(find_all_params, current_user)


@customer_ns.route("/<int:id>")
@customer_ns.param("id", "The customer identifier")
class CustomerResource(Resource):
    @get_resource(customer_ns, customer_model, CustomerNotFound)
    @role_required(UserRole.ADMIN, UserRole.DISTRIBUTOR, UserRole.SELLER)
    def get(self, id: int):
        """Get a customer by ID"""
        current_user = ApiUtils.resolve_current_user()
        return CustomerService.find_first(id, current_user)

    @update_resource(customer_ns, update_customer_model, customer_model, CustomerNotFound)
    @role_required(UserRole.ADMIN, UserRole.DISTRIBUTOR, UserRole.SELLER)
    def patch(self, id: int):
        """Update a customer by ID"""
        current_user = ApiUtils.resolve_current_user()
        return CustomerService.update(id, customer_ns.payload, current_user)

    @deactivate_resource(customer_ns, CustomerNotFound)
    @role_required(UserRole.ADMIN, UserRole.DISTRIBUTOR)
    def delete(self, id: int):
        """Deactivate a customer by ID"""
        current_user = ApiUtils.resolve_current_user()
        CustomerService.deactivate(id, current_user)
        return "", HTTPStatus.NO_CONTENT
