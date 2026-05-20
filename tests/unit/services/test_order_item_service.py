from unittest.mock import patch, MagicMock
import pytest

from app.services import OrderItemService
from app.exceptions import ProductNotFoundException


def test_create_all_staged__returns_order_items(mock_product: MagicMock):
    # A
    item1, item2 = MagicMock(), MagicMock()
    dtos = [
        {"product_id": 1, "quantity": 2, "unit_price": 10.0},
        {"product_id": 2, "quantity": 3, "unit_price": 20.0},
    ]

    p_product = patch(
        "app.services.order_item_service.Product.find_first_by_id",
        return_value=mock_product,
    )
    p_order_item = patch(
        "app.services.order_item_service.OrderItem",
        side_effect=[item1, item2],
    )

    with p_product, p_order_item:
        # A
        result = OrderItemService.create_all_staged(dtos)

        # A
        assert result == [item1, item2]


def test_create_all_staged__raises_if_product_not_found():
    # A
    p_product = patch(
        "app.services.order_item_service.Product.find_first_by_id",
        return_value=None,
    )

    with p_product:
        # A / A
        with pytest.raises(ProductNotFoundException):
            OrderItemService.create_all_staged(
                [{"product_id": 999, "quantity": 1, "unit_price": 10.0}]
            )


def test_create_all_staged__sets_unit_price_from_dto(mock_product: MagicMock):
    # A
    p_product = patch(
        "app.services.order_item_service.Product.find_first_by_id",
        return_value=mock_product,
    )
    p_order_item = patch("app.services.order_item_service.OrderItem")

    with p_product, p_order_item as MockOrderItem:
        # A
        OrderItemService.create_all_staged(
            [{"product_id": 1, "quantity": 2, "unit_price": 49.99}]
        )

        # A
        MockOrderItem.assert_called_once_with(
            product_id=1,
            quantity=2,
            unit_price=49.99,
        )
