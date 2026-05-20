from unittest.mock import patch, MagicMock
import pytest

from app.services import DistributorStockService
from app.exceptions import (
    DistributorStockNotFoundException,
    DistributorStockAlreadyExistsException,
)


def test_create__returns_created_stock(mock_stock: MagicMock):
    # Arrange
    p_stock_cls = patch("app.services.distributor_stock_service.DistributorStock")

    with p_stock_cls as MockStock:
        MockStock.find_first_by_product_and_distributor_ids.return_value = None
        MockStock.return_value = mock_stock

        # Act
        result = DistributorStockService.create({"product_id": 1, "distributor_id": 1})

        # Assert
        assert result == mock_stock


def test_create__raises_if_stock_already_exists(mock_stock: MagicMock):
    # A
    p_find = patch(
        "app.services.distributor_stock_service.DistributorStock.find_first_by_product_and_distributor_ids",
        return_value=mock_stock,
    )

    with p_find:
        # A / A
        with pytest.raises(DistributorStockAlreadyExistsException):
            DistributorStockService.create({"product_id": 1, "distributor_id": 1})


def test_find_first__returns_stock(mock_stock: MagicMock):
    # A
    p_find = patch(
        "app.services.distributor_stock_service.DistributorStock.find_first_by_id",
        return_value=mock_stock,
    )

    with p_find:
        # A
        result = DistributorStockService.find_first(mock_stock.id, {})

        # A
        assert result == mock_stock


def test_find_first__returns_none_if_not_found():
    # A
    p_find = patch(
        "app.services.distributor_stock_service.DistributorStock.find_first_by_id",
        return_value=None,
    )

    with p_find:
        # A
        result = DistributorStockService.find_first(999, {})

        # A
        assert result is None


def test_find_first_or_raise__returns_stock(mock_stock: MagicMock):
    # A
    p_find = patch(
        "app.services.distributor_stock_service.DistributorStockService.find_first",
        return_value=mock_stock,
    )

    with p_find:
        # A
        result = DistributorStockService.find_first_or_raise(mock_stock.id, {})

        # A
        assert result == mock_stock


def test_find_first_or_raise__raises_if_not_found():
    # A
    p_find = patch(
        "app.services.distributor_stock_service.DistributorStockService.find_first",
        return_value=None,
    )

    with p_find:
        # A / A
        with pytest.raises(DistributorStockNotFoundException):
            DistributorStockService.find_first_or_raise(999, {})


def test_find_all__returns_list(mock_stock: MagicMock):
    # A
    params = MagicMock()
    p_find = patch(
        "app.services.distributor_stock_service.DistributorStock.find_all",
        return_value=[mock_stock],
    )

    with p_find as mock_find_all:
        # A
        result = DistributorStockService.find_all(params, {})

        # A
        assert result == [mock_stock]
        mock_find_all.assert_called_once_with(params, {})


def test_find_all_below_minimum__returns_list(mock_stock: MagicMock):
    # A
    p_find = patch(
        "app.services.distributor_stock_service.DistributorStock.find_all_below_minimum",
        return_value=[mock_stock],
    )

    with p_find as mock_find_all:
        # A
        result = DistributorStockService.find_all_below_minimum({"distributor_id": 1})

        # A
        assert result == [mock_stock]
        mock_find_all.assert_called_once_with({"distributor_id": 1})


def test_update__returns_updated_stock(mock_stock: MagicMock):
    # A
    p_find = patch(
        "app.services.distributor_stock_service.DistributorStockService.find_first_or_raise",
        return_value=mock_stock,
    )
    p_save = patch("app.services.distributor_stock_service.DistributorStock.save")

    with p_find, p_save:
        # A
        result = DistributorStockService.update(
            mock_stock.id, {"current_quantity": 20}, {}
        )

        # A
        assert result == mock_stock


def test_update__raises_if_not_found():
    # A
    p_find = patch(
        "app.services.distributor_stock_service.DistributorStockService.find_first_or_raise",
        side_effect=DistributorStockNotFoundException,
    )

    with p_find:
        # A / A
        with pytest.raises(DistributorStockNotFoundException):
            DistributorStockService.update(999, {"current_quantity": 20}, {})


def test_delete__deletes_stock(mock_stock: MagicMock):
    # A
    p_find = patch(
        "app.services.distributor_stock_service.DistributorStockService.find_first_or_raise",
        return_value=mock_stock,
    )
    p_delete = patch("app.services.distributor_stock_service.DistributorStock.delete")

    with p_find, p_delete as mock_delete:
        # A
        DistributorStockService.delete(mock_stock.id, {})

        # A
        mock_delete.assert_called_once_with(mock_stock)


def test_delete__raises_if_not_found():
    # A
    p_find = patch(
        "app.services.distributor_stock_service.DistributorStockService.find_first_or_raise",
        side_effect=DistributorStockNotFoundException,
    )

    with p_find:
        # A / A
        with pytest.raises(DistributorStockNotFoundException):
            DistributorStockService.delete(999, {})


def test_deduct_all_staged__deducts_quantity_for_each_item():
    # A
    item1, item2 = MagicMock(), MagicMock()
    item1.product_id, item1.quantity = 1, 10
    item2.product_id, item2.quantity = 2, 5

    stock1, stock2 = MagicMock(), MagicMock()
    stock1.current_quantity = 50
    stock2.current_quantity = 30

    p_find = patch(
        "app.services.distributor_stock_service.DistributorStock.find_first_by_product_and_distributor_ids",
        side_effect=[stock1, stock2],
    )
    p_db = patch("app.services.distributor_stock_service.db")

    with p_find, p_db:
        # A
        DistributorStockService.deduct_all_staged([item1, item2], distributor_id=1)

        # A
        assert stock1.current_quantity == 40
        assert stock2.current_quantity == 25


def test_deduct_all_staged__does_not_go_below_zero():
    # A
    item = MagicMock()
    item.product_id, item.quantity = 1, 100

    stock = MagicMock()
    stock.current_quantity = 50

    p_find = patch(
        "app.services.distributor_stock_service.DistributorStock.find_first_by_product_and_distributor_ids",
        return_value=stock,
    )
    p_db = patch("app.services.distributor_stock_service.db")

    with p_find, p_db:
        # A
        DistributorStockService.deduct_all_staged([item], distributor_id=1)

        # A
        assert stock.current_quantity == 0


def test_deduct_all_staged__raises_if_stock_not_found():
    # A
    item = MagicMock()
    item.product_id, item.quantity = 1, 10

    p_find = patch(
        "app.services.distributor_stock_service.DistributorStock.find_first_by_product_and_distributor_ids",
        return_value=None,
    )
    p_db = patch("app.services.distributor_stock_service.db")

    with p_find, p_db:
        # A / A
        with pytest.raises(DistributorStockNotFoundException):
            DistributorStockService.deduct_all_staged([item], distributor_id=1)


def test_restore_all_staged__restores_quantity_for_each_item():
    # A
    item1, item2 = MagicMock(), MagicMock()
    item1.product_id, item1.quantity = 1, 10
    item2.product_id, item2.quantity = 2, 5

    stock1, stock2 = MagicMock(), MagicMock()
    stock1.current_quantity = 50
    stock2.current_quantity = 30

    p_find = patch(
        "app.services.distributor_stock_service.DistributorStock.find_first_by_product_and_distributor_ids",
        side_effect=[stock1, stock2],
    )
    p_db = patch("app.services.distributor_stock_service.db")

    with p_find, p_db:
        # A
        DistributorStockService.restore_all_staged([item1, item2], distributor_id=1)

        # A
        assert stock1.current_quantity == 60
        assert stock2.current_quantity == 35


def test_restore_all_staged__raises_if_stock_not_found():
    # A
    item = MagicMock()
    item.product_id, item.quantity = 1, 10

    p_find = patch(
        "app.services.distributor_stock_service.DistributorStock.find_first_by_product_and_distributor_ids",
        return_value=None,
    )
    p_db = patch("app.services.distributor_stock_service.db")

    with p_find, p_db:
        # A / A
        with pytest.raises(DistributorStockNotFoundException):
            DistributorStockService.restore_all_staged([item], distributor_id=1)
