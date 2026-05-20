from unittest.mock import patch, MagicMock
import pytest

from app.services import OrderService
from app.exceptions import (
    CustomerNotFoundException,
    DelinquentCustomerException,
    InvalidOrderStatusTransitionException,
    OrderDeletionNotAllowedException,
    OrderNotFoundException,
)
from app.types import OrderStatus


def test_create__returns_created_order(
    mock_customer: MagicMock,
    mock_order: MagicMock,
):
    # Arrange
    mock_items = [MagicMock()]
    dto = {"customer_id": 1, "distributor_id": 1, "items": mock_items}

    p_customer = patch(
        "app.services.order_service.CustomerService.find_first_or_raise",
        return_value=mock_customer,
    )
    p_order_cls = patch("app.services.order_service.Order")
    p_items = patch(
        "app.services.order_service.OrderItemService.create_all_staged",
        return_value=mock_items,
    )
    p_deduct = patch("app.services.order_service.DistributorStockService.deduct_all_staged")
    p_db = patch("app.services.order_service.db")

    with p_customer, p_order_cls as MockOrder, p_items, p_deduct, p_db:
        MockOrder.find_first_delivered_unpaid_by_customer_id.return_value = None
        MockOrder.return_value = mock_order

        # Act
        result = OrderService.create(dto, {})

        # Assert
        assert result == mock_order


def test_create__raises_if_customer_not_found():
    # A
    p_customer = patch(
        "app.services.order_service.CustomerService.find_first_or_raise",
        side_effect=CustomerNotFoundException,
    )

    with p_customer:
        # A / A
        with pytest.raises(CustomerNotFoundException):
            OrderService.create(
                {"customer_id": 999, "distributor_id": 1, "items": []}, {}
            )


def test_create__raises_if_customer_is_delinquent(
    mock_customer: MagicMock,
    mock_order: MagicMock,
):
    # A
    p_customer = patch(
        "app.services.order_service.CustomerService.find_first_or_raise",
        return_value=mock_customer,
    )
    p_du_order = patch(
        "app.services.order_service.Order.find_first_delivered_unpaid_by_customer_id",
        return_value=mock_order,
    )

    with p_customer, p_du_order:
        # A / A
        with pytest.raises(DelinquentCustomerException):
            OrderService.create(
                {"customer_id": 1, "distributor_id": 1, "items": []}, {}
            )


def test_create__deducts_stock_for_each_item(
    mock_customer: MagicMock,
    mock_order: MagicMock,
):
    # A
    mock_items = [MagicMock()]
    dto = {"customer_id": 1, "distributor_id": 1, "items": mock_items}

    p_customer = patch(
        "app.services.order_service.CustomerService.find_first_or_raise",
        return_value=mock_customer,
    )
    p_order_cls = patch("app.services.order_service.Order")
    p_items = patch(
        "app.services.order_service.OrderItemService.create_all_staged",
        return_value=mock_items,
    )
    p_deduct = patch("app.services.order_service.DistributorStockService.deduct_all_staged")
    p_db = patch("app.services.order_service.db")

    with p_customer, p_order_cls as MockOrder, p_items, p_deduct as mock_deduct, p_db:
        MockOrder.find_first_delivered_unpaid_by_customer_id.return_value = None
        MockOrder.return_value = mock_order

        # A
        OrderService.create(dto, {})

        # A
        mock_deduct.assert_called_once_with(mock_items, mock_order.distributor_id)


def test_find_first__returns_order(mock_order: MagicMock):
    # A
    p_find = patch(
        "app.services.order_service.Order.find_first_by_id",
        return_value=mock_order,
    )

    with p_find:
        # A
        result = OrderService.find_first(mock_order.id, {})

        # A
        assert result == mock_order


def test_find_first__returns_none_if_not_found():
    # A
    p_find = patch(
        "app.services.order_service.Order.find_first_by_id",
        return_value=None,
    )

    with p_find:
        # A
        result = OrderService.find_first(999, {})

        # A
        assert result is None


def test_find_first_or_raise__returns_order(mock_order: MagicMock):
    # A
    p_find = patch(
        "app.services.order_service.OrderService.find_first",
        return_value=mock_order,
    )

    with p_find:
        # A
        result = OrderService.find_first_or_raise(mock_order.id, {})

        # A
        assert result == mock_order


def test_find_first_or_raise__raises_if_not_found():
    # A
    p_find = patch(
        "app.services.order_service.OrderService.find_first",
        return_value=None,
    )

    with p_find:
        # A / A
        with pytest.raises(OrderNotFoundException):
            OrderService.find_first_or_raise(999, {})


def test_find_all__returns_list(mock_order: MagicMock):
    # A
    params = MagicMock()
    p_find = patch(
        "app.services.order_service.Order.find_all",
        return_value=[mock_order],
    )

    with p_find as mock_find_all:
        # A
        result = OrderService.find_all(params, {})

        # A
        assert result == [mock_order]
        mock_find_all.assert_called_once_with(params, {})


def test_update_status__returns_order_with_new_status(mock_order: MagicMock):
    # A
    mock_order.can_transition_to.return_value = True
    mock_order.is_cancelled = False

    p_find = patch(
        "app.services.order_service.OrderService.find_first_or_raise",
        return_value=mock_order,
    )
    p_db = patch("app.services.order_service.db")

    with p_find, p_db:
        # A
        result = OrderService.update_status(
            mock_order.id, {"status": OrderStatus.DELIVERED_PAID}, {}
        )

        # A
        assert result == mock_order


def test_update_status__raises_if_order_not_found():
    # A
    p_find = patch(
        "app.services.order_service.OrderService.find_first_or_raise",
        side_effect=OrderNotFoundException,
    )

    with p_find:
        # A / A
        with pytest.raises(OrderNotFoundException):
            OrderService.update_status(999, {"status": OrderStatus.DELIVERED_PAID}, {})


def test_update_status__raises_if_transition_invalid(mock_order: MagicMock):
    # A
    mock_order.can_transition_to.return_value = False

    p_find = patch(
        "app.services.order_service.OrderService.find_first_or_raise",
        return_value=mock_order,
    )

    with p_find:
        # A / A
        with pytest.raises(InvalidOrderStatusTransitionException):
            OrderService.update_status(
                mock_order.id,
                {"status": OrderStatus.CANCELLED},
                {},
            )


def test_update_status__restores_stock_if_cancelled(mock_order: MagicMock):
    # A
    mock_order.can_transition_to.return_value = True
    mock_order.is_cancelled = True
    mock_order.items = [MagicMock()]

    p_find = patch(
        "app.services.order_service.OrderService.find_first_or_raise",
        return_value=mock_order,
    )
    p_restore = patch("app.services.order_service.DistributorStockService.restore_all_staged")
    p_db = patch("app.services.order_service.db")

    with p_find, p_restore as mock_restore, p_db:
        # A
        OrderService.update_status(mock_order.id, {"status": OrderStatus.CANCELLED}, {})

        # A
        mock_restore.assert_called_once_with(
            mock_order.items, mock_order.distributor_id
        )


def test_delete__deletes_cancelled_order(mock_order: MagicMock):
    # A
    mock_order.is_cancelled = True

    p_find = patch(
        "app.services.order_service.OrderService.find_first_or_raise",
        return_value=mock_order,
    )
    p_delete = patch("app.services.order_service.Order.delete")

    with p_find, p_delete as mock_delete:
        # A
        OrderService.delete(mock_order.id, {})

        # A
        mock_delete.assert_called_once_with(mock_order)


def test_delete__raises_if_order_not_found():
    # A
    p_find = patch(
        "app.services.order_service.OrderService.find_first_or_raise",
        side_effect=OrderNotFoundException,
    )

    with p_find:
        # A / A
        with pytest.raises(OrderNotFoundException):
            OrderService.delete(999, {})


def test_delete__raises_if_order_not_cancelled(mock_order: MagicMock):
    # A
    mock_order.is_cancelled = False

    p_find = patch(
        "app.services.order_service.OrderService.find_first_or_raise",
        return_value=mock_order,
    )

    with p_find:
        # A / A
        with pytest.raises(OrderDeletionNotAllowedException):
            OrderService.delete(mock_order.id, {})
