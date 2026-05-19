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
from app.exceptions import ProductNotFound, SkuAlreadyInUse
from app.factories import FindAllFactory
from app.services import ProductService
from app.types import UserRole

from . import product_ns
from .models import create_product_model, product_model, update_product_model


@product_ns.route("/")
class ProductListResource(Resource):
    __find_all_parser = FindAllFactory.build_find_all_parser(product_ns)

    @create_resource(
        product_ns,
        create_product_model,
        product_model,
        SkuAlreadyInUse,
    )
    @auth_required(UserRole.ADMIN)
    def post(self, **_):
        """Create a new product"""
        return ProductService.create(product_ns.payload), HTTPStatus.CREATED

    @list_resource(product_ns, __find_all_parser, product_model)
    @auth_required(UserRole.ADMIN, UserRole.DISTRIBUTOR, UserRole.SELLER)
    def get(self, **_):
        """Get all products"""
        find_all_params = FindAllFactory.build_find_all_params(self.__find_all_parser)
        return ProductService.find_all(find_all_params)


@product_ns.route("/<int:id>")
@product_ns.param("id", "The product identifier")
class ProductResource(Resource):
    @get_resource(product_ns, product_model, ProductNotFound)
    @auth_required(UserRole.ADMIN, UserRole.DISTRIBUTOR, UserRole.SELLER)
    def get(self, id: int, **_):
        """Get a product by ID"""
        return ProductService.find_first_or_raise(id)

    @update_resource(
        product_ns,
        update_product_model,
        product_model,
        ProductNotFound,
        SkuAlreadyInUse,
    )
    @auth_required(UserRole.ADMIN)
    def patch(self, id: int, **_):
        """Update a product by ID"""
        return ProductService.update(id, product_ns.payload)

    # @delete_resource(product_ns, ProductNotFound)
    # @auth_required(UserRole.ADMIN)
    # def delete(self, id: int, **_):
    #     """Delete a product by ID"""
    #     ProductService.delete(id)
    #     return "", HTTPStatus.NO_CONTENT
