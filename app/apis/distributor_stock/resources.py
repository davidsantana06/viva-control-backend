from flask_restx import Resource
from http import HTTPStatus

from app.decorators import (
    create_resource,
    delete_resource,
    get_resource,
    list_resource,
    role_required,
    update_resource,
)
from app.exceptions import DistributorStockNotFound, DistributorStockAlreadyExists
from app.factories import FindAllFactory
from app.services import DistributorStockService
from app.types import UserRole
from app.utils import ApiUtils

from . import distributor_stock_ns
from .models import (
    create_distributor_stock_model,
    distributor_stock_model,
    update_distributor_stock_model,
)


@distributor_stock_ns.route("/")
class DistributorStockList(Resource):
    __find_all_parser = FindAllFactory.build_find_all_parser(distributor_stock_ns)

    @create_resource(
        distributor_stock_ns,
        create_distributor_stock_model,
        distributor_stock_model,
        DistributorStockAlreadyExists,
    )
    @role_required(UserRole.DISTRIBUTOR)
    def post(self):
        """Create a new stock entry"""
        current_user = ApiUtils.resolve_current_user()
        return (
            DistributorStockService.create(distributor_stock_ns.payload, current_user),
            HTTPStatus.CREATED,
        )

    @list_resource(distributor_stock_ns, __find_all_parser, distributor_stock_model)
    @role_required(UserRole.ADMIN, UserRole.DISTRIBUTOR, UserRole.SELLER)
    def get(self):
        """Get all stock entries"""
        current_user = ApiUtils.resolve_current_user()
        find_all_params = FindAllFactory.build_find_all_params(self.__find_all_parser)
        return DistributorStockService.find_all(find_all_params, current_user)


@distributor_stock_ns.route("/below-minimum")
class DistributorStockBelowMinimum(Resource):
    @distributor_stock_ns.doc("list_below_minimum", security="Bearer")
    @distributor_stock_ns.marshal_list_with(distributor_stock_model)
    @role_required(UserRole.ADMIN, UserRole.DISTRIBUTOR)
    def get(self):
        """Get stock entries at or below minimum quantity"""
        current_user = ApiUtils.resolve_current_user()
        return DistributorStockService.find_all_below_minimum(current_user)


@distributor_stock_ns.route("/<int:id>")
@distributor_stock_ns.param("id", "The stock entry identifier")
class DistributorStockResource(Resource):
    @get_resource(
        distributor_stock_ns,
        distributor_stock_model,
        DistributorStockNotFound,
    )
    @role_required(UserRole.ADMIN, UserRole.DISTRIBUTOR, UserRole.SELLER)
    def get(self, id: int):
        """Get a stock entry by ID"""
        current_user = ApiUtils.resolve_current_user()
        return DistributorStockService.find_first(id, current_user)

    @update_resource(
        distributor_stock_ns,
        update_distributor_stock_model,
        distributor_stock_model,
        DistributorStockNotFound,
    )
    @role_required(UserRole.DISTRIBUTOR)
    def patch(self, id: int):
        """Update a stock entry by ID"""
        current_user = ApiUtils.resolve_current_user()
        return DistributorStockService.update(
            id,
            distributor_stock_ns.payload,
            current_user,
        )

    # @delete_resource(distributor_stock_ns, DistributorStockNotFound)
    # @role_required(UserRole.DISTRIBUTOR)
    # def delete(self, id: int):
    #     """Delete a stock entry by ID"""
    #     current_user = ApiUtils.resolve_current_user()
    #     DistributorStockService.delete(id, current_user)
    #     return "", HTTPStatus.NO_CONTENT
