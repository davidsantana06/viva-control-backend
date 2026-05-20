from unittest.mock import patch, MagicMock
import pytest

from app.services import ProductService
from app.exceptions import ProductNotFoundException, SkuAlreadyInUseException


def test_create__returns_created_product(mock_product: MagicMock):
    # Arrange
    p_product_cls = patch("app.services.product_service.Product")

    with p_product_cls as MockProduct:
        MockProduct.find_first_by_sku.return_value = None
        MockProduct.return_value = mock_product

        # Act
        result = ProductService.create(
            {"sku": "SKU-001", "name": "Test", "suggested_price": 10.0}
        )

        # Assert
        assert result == mock_product


def test_create__raises_if_sku_already_in_use(mock_product: MagicMock):
    # A
    p_find = patch(
        "app.services.product_service.Product.find_first_by_sku",
        return_value=mock_product,
    )

    with p_find:
        # A / A
        with pytest.raises(SkuAlreadyInUseException):
            ProductService.create(
                {"sku": "SKU-001", "name": "Test", "suggested_price": 10.0}
            )


def test_find_first__returns_product(mock_product: MagicMock):
    # A
    p_find = patch(
        "app.services.product_service.Product.find_first_by_id",
        return_value=mock_product,
    )

    with p_find:
        # A
        result = ProductService.find_first(mock_product.id)

        # A
        assert result == mock_product


def test_find_first__returns_none_if_not_found():
    # A
    p_find = patch(
        "app.services.product_service.Product.find_first_by_id",
        return_value=None,
    )

    with p_find:
        # A
        result = ProductService.find_first(999)

        # A
        assert result is None


def test_find_first_or_raise__returns_product(mock_product: MagicMock):
    # A
    p_find = patch(
        "app.services.product_service.ProductService.find_first",
        return_value=mock_product,
    )

    with p_find:
        # A
        result = ProductService.find_first_or_raise(mock_product.id)

        # A
        assert result == mock_product


def test_find_first_or_raise__raises_if_not_found():
    # A
    p_find = patch(
        "app.services.product_service.ProductService.find_first",
        return_value=None,
    )

    with p_find:
        # A / A
        with pytest.raises(ProductNotFoundException):
            ProductService.find_first_or_raise(999)


def test_find_all__returns_list(mock_product: MagicMock):
    # A
    params = MagicMock()
    p_find = patch(
        "app.services.product_service.Product.find_all",
        return_value=[mock_product],
    )

    with p_find as mock_find_all:
        # A
        result = ProductService.find_all(params)

        # A
        assert result == [mock_product]
        mock_find_all.assert_called_once_with(params)


def test_update__returns_updated_product(mock_product: MagicMock):
    # A
    mock_product.sku = "SKU-001"

    p_find = patch(
        "app.services.product_service.ProductService.find_first_or_raise",
        return_value=mock_product,
    )
    p_find_sku = patch(
        "app.services.product_service.Product.find_first_by_sku",
        return_value=None,
    )
    p_save = patch("app.services.product_service.Product.save")

    with p_find, p_find_sku, p_save:
        # A
        result = ProductService.update(
            mock_product.id,
            {"sku": "SKU-002", "name": "Updated", "suggested_price": 20.0},
        )

        # A
        assert result == mock_product


def test_update__raises_if_not_found():
    # A
    p_find = patch(
        "app.services.product_service.ProductService.find_first_or_raise",
        side_effect=ProductNotFoundException,
    )

    with p_find:
        # A / A
        with pytest.raises(ProductNotFoundException):
            ProductService.update(
                999, {"sku": "SKU-002", "name": "Updated", "suggested_price": 20.0}
            )


def test_update__raises_if_new_sku_already_in_use(mock_product: MagicMock):
    # A
    mock_product.sku = "SKU-001"

    p_find = patch(
        "app.services.product_service.ProductService.find_first_or_raise",
        return_value=mock_product,
    )
    p_find_sku = patch(
        "app.services.product_service.Product.find_first_by_sku",
        return_value=MagicMock(),
    )

    with p_find, p_find_sku:
        # A / A
        with pytest.raises(SkuAlreadyInUseException):
            ProductService.update(
                mock_product.id,
                {"sku": "SKU-002", "name": "Updated", "suggested_price": 20.0},
            )


def test_update__does_not_check_sku_if_unchanged(mock_product: MagicMock):
    # A
    mock_product.sku = "SKU-001"

    p_find = patch(
        "app.services.product_service.ProductService.find_first_or_raise",
        return_value=mock_product,
    )
    p_find_sku = patch("app.services.product_service.Product.find_first_by_sku")
    p_save = patch("app.services.product_service.Product.save")

    with p_find, p_find_sku as mock_find_sku, p_save:
        # A
        ProductService.update(
            mock_product.id,
            {"sku": "SKU-001", "name": "Updated", "suggested_price": 20.0},
        )

        # A
        mock_find_sku.assert_not_called()


def test_delete__deletes_product(mock_product: MagicMock):
    # A
    p_find = patch(
        "app.services.product_service.ProductService.find_first_or_raise",
        return_value=mock_product,
    )
    p_delete = patch("app.services.product_service.Product.delete")

    with p_find, p_delete as mock_delete:
        # A
        ProductService.delete(mock_product.id)

        # A
        mock_delete.assert_called_once_with(mock_product)


def test_delete__raises_if_not_found():
    # A
    p_find = patch(
        "app.services.product_service.ProductService.find_first_or_raise",
        side_effect=ProductNotFoundException,
    )

    with p_find:
        # A / A
        with pytest.raises(ProductNotFoundException):
            ProductService.delete(999)
