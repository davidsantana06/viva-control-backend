from flask_restx import Resource
from http import HTTPStatus

from app.decorators import (
    auth_required,
    create_resource,
    delete_resource,
    get_resource,
    list_resource,
    update_resource,
)
from app.exceptions import CustomerNotFound
from app.factories import FindAllFactory, UserFilterFactory
from app.services import CustomerService
from app.types import CurrentUser, UserRole
from app.utils import DtoUtils

from . import customer_ns
from .models import create_customer_model, customer_model, update_customer_model


@customer_ns.route("/")
class CustomerListResource(Resource):
    __find_all_parser = FindAllFactory.build_user_scoped_find_all_parser(customer_ns)

    @create_resource(customer_ns, create_customer_model, customer_model)
    @auth_required(UserRole.DISTRIBUTOR, UserRole.SELLER)
    def post(self, current_user: CurrentUser):
        """Create a new customer"""
        dto = {**customer_ns.payload}
        DtoUtils.inject_user_ids(dto, current_user)
        return CustomerService.create(dto), HTTPStatus.CREATED

    @list_resource(customer_ns, __find_all_parser, customer_model)
    @auth_required(UserRole.ADMIN, UserRole.DISTRIBUTOR, UserRole.SELLER)
    def get(self, current_user: CurrentUser):
        """Get all customers"""
        find_all_params = FindAllFactory.build_user_scoped_find_all_params(
            self.__find_all_parser,
        )
        user_filter = UserFilterFactory.build_user_filter(
            current_user,
            find_all_params.user_scoped,
        )
        return CustomerService.find_all(find_all_params, user_filter)


@customer_ns.route("/<int:id>")
@customer_ns.param("id", "The customer identifier")
class CustomerResource(Resource):
    @get_resource(customer_ns, customer_model, CustomerNotFound)
    @auth_required(UserRole.ADMIN, UserRole.DISTRIBUTOR, UserRole.SELLER)
    def get(self, id: int, current_user: CurrentUser):
        """Get a customer by ID"""
        user_filter = UserFilterFactory.build_user_filter(current_user)
        return CustomerService.find_first_or_raise(id, user_filter)

    @update_resource(
        customer_ns,
        update_customer_model,
        customer_model,
        CustomerNotFound,
    )
    @auth_required(UserRole.DISTRIBUTOR, UserRole.SELLER)
    def patch(self, id: int, current_user: CurrentUser):
        """Update a customer by ID"""
        user_filter = UserFilterFactory.build_user_filter(current_user)
        return CustomerService.update(id, customer_ns.payload, user_filter)

    # @delete_resource(customer_ns, CustomerNotFound)
    # @auth_required(UserRole.DISTRIBUTOR, UserRole.SELLER)
    # def delete(self, id: int, current_user: CurrentUser):
    #     """Delete a customer by ID"""
    #     user_filter = UserFilterFactory.build_user_filter(current_user)
    #     CustomerService.delete(id, user_filter)
    #     return "", HTTPStatus.NO_CONTENT
