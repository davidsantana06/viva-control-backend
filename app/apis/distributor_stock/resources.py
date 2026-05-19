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
from app.exceptions import DistributorStockNotFound, DistributorStockAlreadyExists
from app.factories import FindAllFactory, UserFilterFactory
from app.services import DistributorStockService
from app.types import CurrentUser, UserRole
from app.utils import DtoUtils

from . import distributor_stock_ns
from .models import (
    create_distributor_stock_model,
    distributor_stock_model,
    update_distributor_stock_model,
)


@distributor_stock_ns.route("/")
class DistributorStockListResource(Resource):
    __find_all_parser = FindAllFactory.build_find_all_parser(distributor_stock_ns)

    @create_resource(
        distributor_stock_ns,
        create_distributor_stock_model,
        distributor_stock_model,
        DistributorStockAlreadyExists,
    )
    @auth_required(UserRole.DISTRIBUTOR)
    def post(self, current_user: CurrentUser):
        """Create a new stock entry"""
        dto = {**distributor_stock_ns.payload}
        DtoUtils.inject_user_ids(dto, current_user)
        return DistributorStockService.create(dto), HTTPStatus.CREATED

    @list_resource(distributor_stock_ns, __find_all_parser, distributor_stock_model)
    @auth_required(UserRole.ADMIN, UserRole.DISTRIBUTOR, UserRole.SELLER)
    def get(self, current_user: CurrentUser):
        """Get all stock entries"""
        find_all_params = FindAllFactory.build_find_all_params(self.__find_all_parser)
        user_filter = UserFilterFactory.build_strict_distributor_filter(current_user)
        return DistributorStockService.find_all(find_all_params, user_filter)


@distributor_stock_ns.route("/below-minimum")
class DistributorStockBelowMinimumResource(Resource):
    @distributor_stock_ns.doc("list_below_minimum", security="Bearer")
    @distributor_stock_ns.marshal_list_with(distributor_stock_model)
    @auth_required(UserRole.ADMIN, UserRole.DISTRIBUTOR)
    def get(self, current_user: CurrentUser):
        """Get stock entries at or below minimum quantity"""
        user_filter = UserFilterFactory.build_strict_distributor_filter(current_user)
        return DistributorStockService.find_all_below_minimum(user_filter)


@distributor_stock_ns.route("/<int:id>")
@distributor_stock_ns.param("id", "The stock entry identifier")
class DistributorStockResource(Resource):
    @get_resource(
        distributor_stock_ns,
        distributor_stock_model,
        DistributorStockNotFound,
    )
    @auth_required(UserRole.ADMIN, UserRole.DISTRIBUTOR, UserRole.SELLER)
    def get(self, id: int, current_user: CurrentUser):
        """Get a stock entry by ID"""
        user_filter = UserFilterFactory.build_strict_distributor_filter(current_user)
        return DistributorStockService.find_first_or_raise(id, user_filter)

    @update_resource(
        distributor_stock_ns,
        update_distributor_stock_model,
        distributor_stock_model,
        DistributorStockNotFound,
    )
    @auth_required(UserRole.DISTRIBUTOR)
    def patch(self, id: int, current_user: CurrentUser):
        """Update a stock entry by ID"""
        user_filter = UserFilterFactory.build_strict_distributor_filter(current_user)
        return DistributorStockService.update(
            id,
            distributor_stock_ns.payload,
            user_filter,
        )

    # @delete_resource(distributor_stock_ns, DistributorStockNotFound)
    # @auth_required(UserRole.DISTRIBUTOR)
    # def delete(self, id: int, current_user: CurrentUser):
    #     """Delete a stock entry by ID"""
    #     user_filter = UserFilterFactory.build_strict_distributor_filter(current_user)
    #     DistributorStockService.delete(id, user_filter)
    #     return "", HTTPStatus.NO_CONTENT
