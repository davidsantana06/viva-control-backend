from app.dtos import CreateOrderItemDto
from app.exceptions import ProductNotFoundException
from app.models import OrderItem, Product


class OrderItemService:
    @classmethod
    def create_all_staged(cls, dtos: list[CreateOrderItemDto]) -> list[OrderItem]:
        return [cls.__create_staged(dto) for dto in dtos]

    @staticmethod
    def __create_staged(dto: CreateOrderItemDto) -> OrderItem:
        product = Product.find_first_by_id(dto["product_id"])
        if not product:
            raise ProductNotFoundException()

        return OrderItem(
            product_id=dto["product_id"],
            quantity=dto["quantity"],
            unit_price=dto["unit_price"],
        )
