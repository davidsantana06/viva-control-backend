from app.dtos import CreateProductDto, UpdateProductDto
from app.exceptions import ProductNotFound, SkuAlreadyInUse
from app.models import Product
from app.types import FindAllParams


class ProductService:
    @staticmethod
    def create(dto: CreateProductDto) -> Product:
        other_product = Product.find_first_by_sku(dto["sku"])
        if other_product:
            raise SkuAlreadyInUse()

        product = Product(**dto)
        Product.save(product)
        return product

    @staticmethod
    def find_all(params: FindAllParams) -> list[Product]:
        return Product.find_all(params)

    @staticmethod
    def find_first(id: int) -> Product:
        product = Product.find_first_by_id(id)

        if not product:
            raise ProductNotFound()

        return product

    @classmethod
    def update(cls, id: int, dto: UpdateProductDto) -> Product:
        product = cls.find_first(id)

        sku_is_different = dto["sku"] != product.sku
        other_product = sku_is_different and Product.find_first_by_sku(dto["sku"])
        if other_product:
            raise SkuAlreadyInUse()

        product.update(**dto)
        Product.save(product)
        return product

    @classmethod
    def delete(cls, id: int) -> None:
        product = cls.find_first(id)
        Product.delete(product)
