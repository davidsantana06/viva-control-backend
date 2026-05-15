from flask_restx import Resource
from http import HTTPStatus

from app.decorators import role_required
from app.exceptions import InvalidPayload, ProductNotFound
from app.services import ProductService
from app.types import UserRole
from app.utils import ApiUtils

from . import product_ns
from .models import create_product_model, product_model, update_product_model


@product_ns.route("/")
class ProductList(Resource):
    __find_all_parser = ApiUtils.build_find_all_parser(product_ns)

    @product_ns.doc("create_product")
    @product_ns.expect(create_product_model)
    @product_ns.marshal_with(product_model, code=HTTPStatus.CREATED)
    @product_ns.response(*InvalidPayload.get_specs())
    @role_required(UserRole.ADMIN)
    def post(self):
        """Create a new product"""
        return ProductService.create(product_ns.payload), HTTPStatus.CREATED

    @product_ns.doc("list_products")
    @product_ns.expect(__find_all_parser)
    @product_ns.marshal_list_with(product_model)
    @role_required(UserRole.ADMIN, UserRole.DISTRIBUTOR, UserRole.SELLER)
    def get(self):
        """Get all products"""
        find_all_params = ApiUtils.build_find_all_params(self.__find_all_parser)
        return ProductService.find_all(find_all_params)


@product_ns.route("/<int:id>")
@product_ns.param("id", "The product identifier")
@product_ns.response(*ProductNotFound.get_specs())
class Product(Resource):
    @product_ns.doc("get_product")
    @product_ns.marshal_with(product_model)
    @role_required(UserRole.ADMIN, UserRole.DISTRIBUTOR, UserRole.SELLER)
    def get(self, id: int):
        """Get a product by ID"""
        return ProductService.find_first(id)

    @product_ns.doc("update_product")
    @product_ns.expect(update_product_model)
    @product_ns.marshal_with(product_model)
    @product_ns.response(*InvalidPayload.get_specs())
    @role_required(UserRole.ADMIN)
    def patch(self, id: int):
        """Update a product by ID"""
        return ProductService.update(id, product_ns.payload)

    @product_ns.doc("deactivate_product")
    @product_ns.response(HTTPStatus.NO_CONTENT, "Success")
    @role_required(UserRole.ADMIN)
    def delete(self, id: int):
        """Deactivate a product by ID"""
        ProductService.deactivate(id)
        return "", HTTPStatus.NO_CONTENT
