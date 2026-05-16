from app.dtos import CreateProductDto, UpdateProductDto
from app.exceptions import ProductNotFound, SkuAlreadyInUse
from app.models import Product
from app.types import FindAllParams


class ProductService:
    @staticmethod
    def create(dto: CreateProductDto) -> Product:
        if Product.find_first_by_sku(dto["sku"]):
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

        sku_already_in_use = dto["sku"] != product.sku and Product.find_first_by_sku(dto["sku"])
        if sku_already_in_use:
            raise SkuAlreadyInUse()

        product.update(**dto)
        Product.save(product)
        return product

    @classmethod
    def deactivate(cls, id: int) -> None:
        product = cls.find_first(id)
        Product.deactivate(product)
        Product.save(product)
