from unittest.mock import patch, MagicMock
import pytest

from app.services import CustomerService
from app.exceptions import CustomerNotFoundException


def test_create__returns_created_customer(mock_customer: MagicMock):
    # A
    p_customer_cls = patch("app.services.customer_service.Customer")

    with p_customer_cls as MockCustomer:
        MockCustomer.return_value = mock_customer

        # A
        result = CustomerService.create({"name": "Test", "distributor_id": 1})

        # A
        assert result == mock_customer


def test_find_first__returns_customer(mock_customer: MagicMock):
    # A
    p_find = patch(
        "app.services.customer_service.Customer.find_first_by_id",
        return_value=mock_customer,
    )

    with p_find:
        # A
        result = CustomerService.find_first(mock_customer.id, {})

        # A
        assert result == mock_customer


def test_find_first__returns_none_if_not_found():
    # A
    p_find = patch(
        "app.services.customer_service.Customer.find_first_by_id",
        return_value=None,
    )

    with p_find:
        # A
        result = CustomerService.find_first(999, {})

        # A
        assert result is None


def test_find_first_or_raise__returns_customer(mock_customer: MagicMock):
    # A
    p_find = patch(
        "app.services.customer_service.CustomerService.find_first",
        return_value=mock_customer,
    )

    with p_find:
        # A
        result = CustomerService.find_first_or_raise(mock_customer.id, {})

        # A
        assert result == mock_customer


def test_find_first_or_raise__raises_if_not_found():
    # A
    p_find = patch(
        "app.services.customer_service.CustomerService.find_first",
        return_value=None,
    )

    with p_find:
        # A / A
        with pytest.raises(CustomerNotFoundException):
            CustomerService.find_first_or_raise(999, {})


def test_find_all__returns_list(mock_customer: MagicMock):
    # A
    params = MagicMock()
    p_find = patch(
        "app.services.customer_service.Customer.find_all",
        return_value=[mock_customer],
    )

    with p_find as mock_find_all:
        # A
        result = CustomerService.find_all(params, {})

        # A
        assert result == [mock_customer]
        mock_find_all.assert_called_once_with(params, {})


def test_update__returns_updated_customer(mock_customer: MagicMock):
    # A
    p_find = patch(
        "app.services.customer_service.CustomerService.find_first_or_raise",
        return_value=mock_customer,
    )
    p_save = patch("app.services.customer_service.Customer.save")

    with p_find, p_save:
        # A
        result = CustomerService.update(mock_customer.id, {"name": "Updated"}, {})

        # A
        assert result == mock_customer


def test_update__raises_if_not_found():
    # A
    p_find = patch(
        "app.services.customer_service.CustomerService.find_first_or_raise",
        side_effect=CustomerNotFoundException,
    )

    with p_find:
        # A / A
        with pytest.raises(CustomerNotFoundException):
            CustomerService.update(999, {"name": "Updated"}, {})


def test_delete__deletes_customer(mock_customer: MagicMock):
    # A
    p_find = patch(
        "app.services.customer_service.CustomerService.find_first_or_raise",
        return_value=mock_customer,
    )
    p_delete = patch("app.services.customer_service.Customer.delete")

    with p_find, p_delete as mock_delete:
        # A
        CustomerService.delete(mock_customer.id, {})

        # A
        mock_delete.assert_called_once_with(mock_customer)


def test_delete__raises_if_not_found():
    # A
    p_find = patch(
        "app.services.customer_service.CustomerService.find_first_or_raise",
        side_effect=CustomerNotFoundException,
    )

    with p_find:
        # A / A
        with pytest.raises(CustomerNotFoundException):
            CustomerService.delete(999, {})
