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
from app.exceptions import ProductNotFound, ProductSkuAlreadyInUse
from app.services import ProductService
from app.types import UserRole
from app.utils import ApiUtils

from . import product_ns
from .models import create_product_model, product_model, update_product_model


@product_ns.route("/")
class ProductList(Resource):
    __find_all_parser = ApiUtils.build_find_all_parser(product_ns)

    @create_resource(
        product_ns,
        create_product_model,
        product_model,
        ProductSkuAlreadyInUse,
    )
    @role_required(UserRole.ADMIN)
    def post(self):
        """Create a new product"""
        return ProductService.create(product_ns.payload), HTTPStatus.CREATED

    @list_resource(product_ns, __find_all_parser, product_model)
    @role_required(UserRole.ADMIN, UserRole.DISTRIBUTOR, UserRole.SELLER)
    def get(self):
        """Get all products"""
        find_all_params = ApiUtils.build_find_all_params(self.__find_all_parser)
        return ProductService.find_all(find_all_params)


@product_ns.route("/<int:id>")
@product_ns.param("id", "The product identifier")
class Product(Resource):
    @get_resource(product_ns, product_model, ProductNotFound)
    @role_required(UserRole.ADMIN, UserRole.DISTRIBUTOR, UserRole.SELLER)
    def get(self, id: int):
        """Get a product by ID"""
        return ProductService.find_first(id)

    @update_resource(
        product_ns,
        update_product_model,
        product_model,
        ProductNotFound,
        ProductSkuAlreadyInUse,
    )
    @role_required(UserRole.ADMIN)
    def patch(self, id: int):
        """Update a product by ID"""
        return ProductService.update(id, product_ns.payload)

    @deactivate_resource(product_ns, ProductNotFound)
    @role_required(UserRole.ADMIN)
    def delete(self, id: int):
        """Deactivate a product by ID"""
        ProductService.deactivate(id)
        return "", HTTPStatus.NO_CONTENT
