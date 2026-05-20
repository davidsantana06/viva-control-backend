from unittest.mock import patch, MagicMock
import pytest

from app.services import PaymentMethodService
from app.exceptions import PaymentMethodNotFoundException


def test_create__returns_created_payment_method(mock_payment_method: MagicMock):
    # A
    p_pm_cls = patch("app.services.payment_method_service.PaymentMethod")

    with p_pm_cls as MockPaymentMethod:
        MockPaymentMethod.return_value = mock_payment_method

        # A
        result = PaymentMethodService.create({"name": "Dinheiro"})

        # A
        assert result == mock_payment_method


def test_find_first__returns_payment_method(mock_payment_method: MagicMock):
    # A
    p_find = patch(
        "app.services.payment_method_service.PaymentMethod.find_first_by_id",
        return_value=mock_payment_method,
    )

    with p_find:
        # A
        result = PaymentMethodService.find_first(mock_payment_method.id)

        # A
        assert result == mock_payment_method


def test_find_first__returns_none_if_not_found():
    # A
    p_find = patch(
        "app.services.payment_method_service.PaymentMethod.find_first_by_id",
        return_value=None,
    )

    with p_find:
        # A
        result = PaymentMethodService.find_first(999)

        # A
        assert result is None


def test_find_first_or_raise__returns_payment_method(mock_payment_method: MagicMock):
    # A
    p_find = patch(
        "app.services.payment_method_service.PaymentMethodService.find_first",
        return_value=mock_payment_method,
    )

    with p_find:
        # A
        result = PaymentMethodService.find_first_or_raise(mock_payment_method.id)

        # A
        assert result == mock_payment_method


def test_find_first_or_raise__raises_if_not_found():
    # A
    p_find = patch(
        "app.services.payment_method_service.PaymentMethodService.find_first",
        return_value=None,
    )

    with p_find:
        # A / A
        with pytest.raises(PaymentMethodNotFoundException):
            PaymentMethodService.find_first_or_raise(999)


def test_find_all__returns_list(mock_payment_method: MagicMock):
    # A
    params = MagicMock()
    p_find = patch(
        "app.services.payment_method_service.PaymentMethod.find_all",
        return_value=[mock_payment_method],
    )

    with p_find as mock_find_all:
        # A
        result = PaymentMethodService.find_all(params)

        # A
        assert result == [mock_payment_method]
        mock_find_all.assert_called_once_with(params)


def test_update__returns_updated_payment_method(mock_payment_method: MagicMock):
    # A
    p_find = patch(
        "app.services.payment_method_service.PaymentMethodService.find_first_or_raise",
        return_value=mock_payment_method,
    )
    p_save = patch("app.services.payment_method_service.PaymentMethod.save")

    with p_find, p_save:
        # A
        result = PaymentMethodService.update(mock_payment_method.id, {"name": "Pix"})

        # A
        assert result == mock_payment_method


def test_update__raises_if_not_found():
    # A
    p_find = patch(
        "app.services.payment_method_service.PaymentMethodService.find_first_or_raise",
        side_effect=PaymentMethodNotFoundException,
    )

    with p_find:
        # A / A
        with pytest.raises(PaymentMethodNotFoundException):
            PaymentMethodService.update(999, {"name": "Pix"})


def test_delete__deletes_payment_method(mock_payment_method: MagicMock):
    # A
    p_find = patch(
        "app.services.payment_method_service.PaymentMethodService.find_first_or_raise",
        return_value=mock_payment_method,
    )
    p_delete = patch("app.services.payment_method_service.PaymentMethod.delete")

    with p_find, p_delete as mock_delete:
        # A
        PaymentMethodService.delete(mock_payment_method.id)

        # A
        mock_delete.assert_called_once_with(mock_payment_method)


def test_delete__raises_if_not_found():
    # A
    p_find = patch(
        "app.services.payment_method_service.PaymentMethodService.find_first_or_raise",
        side_effect=PaymentMethodNotFoundException,
    )

    with p_find:
        # A / A
        with pytest.raises(PaymentMethodNotFoundException):
            PaymentMethodService.delete(999)
