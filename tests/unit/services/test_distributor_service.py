from unittest.mock import patch, MagicMock
import pytest

from app.services import DistributorService
from app.exceptions import UserNotFoundException
from app.types import UserRole


def test_find_first__returns_distributor(mock_user: MagicMock):
    # Arrange
    p_find = patch(
        "app.services.distributor_service.User.find_first_by_id_and_role",
        return_value=mock_user,
    )

    with p_find:
        # Act
        result = DistributorService.find_first(mock_user.id)

        # Assert
        assert result == mock_user


def test_find_first__returns_none_if_not_found():
    # A
    p_find = patch(
        "app.services.distributor_service.User.find_first_by_id_and_role",
        return_value=None,
    )

    with p_find:
        # A
        result = DistributorService.find_first(999)

        # A
        assert result is None


def test_find_first_or_raise__returns_distributor(mock_user: MagicMock):
    # A
    p_find = patch(
        "app.services.distributor_service.DistributorService.find_first",
        return_value=mock_user,
    )

    with p_find:
        # A
        result = DistributorService.find_first_or_raise(mock_user.id)

        # A
        assert result == mock_user


def test_find_first_or_raise__raises_if_not_found():
    # A
    p_find = patch(
        "app.services.distributor_service.DistributorService.find_first",
        return_value=None,
    )

    with p_find:
        # A / A
        with pytest.raises(UserNotFoundException):
            DistributorService.find_first_or_raise(999)


def test_find_all__returns_list(mock_user: MagicMock):
    # A
    params = MagicMock()
    p_find = patch(
        "app.services.distributor_service.User.find_all_by_role",
        return_value=[mock_user],
    )

    with p_find as mock_find_all:
        # A
        result = DistributorService.find_all(params)

        # A
        assert result == [mock_user]
        mock_find_all.assert_called_once_with(params, {}, role=UserRole.DISTRIBUTOR)


def test_activate__raises_if_distributor_not_found():
    # A
    p_find = patch(
        "app.services.distributor_service.DistributorService.find_first_or_raise",
        side_effect=UserNotFoundException,
    )

    with p_find:
        # A / A
        with pytest.raises(UserNotFoundException):
            DistributorService.activate(999)


def test_activate__toggles_each_seller_staged(mock_user: MagicMock):
    # A
    seller1, seller2 = MagicMock(), MagicMock()
    mock_user.sellers = [seller1, seller2]

    p_find = patch(
        "app.services.distributor_service.DistributorService.find_first_or_raise",
        return_value=mock_user,
    )
    p_toggle_staged = patch(
        "app.services.distributor_service.User.toggle_activation_staged"
    )
    p_toggle = patch("app.services.distributor_service.User.toggle_activation")
    p_db = patch("app.services.distributor_service.db")

    with p_find, p_toggle_staged as mock_toggle_staged, p_toggle, p_db:
        # A
        DistributorService.activate(mock_user.id)

        # A
        mock_toggle_staged.assert_any_call(seller1)
        mock_toggle_staged.assert_any_call(seller2)


def test_activate__toggles_distributor_activation(mock_user: MagicMock):
    # A
    mock_user.sellers = []

    p_find = patch(
        "app.services.distributor_service.DistributorService.find_first_or_raise",
        return_value=mock_user,
    )
    p_toggle_staged = patch(
        "app.services.distributor_service.User.toggle_activation_staged"
    )
    p_toggle = patch("app.services.distributor_service.User.toggle_activation")
    p_db = patch("app.services.distributor_service.db")

    with p_find, p_toggle_staged, p_toggle as mock_toggle, p_db:
        # A
        DistributorService.activate(mock_user.id)

        # A
        mock_toggle.assert_called_once_with(mock_user)


def test_deactivate__raises_if_distributor_not_found():
    # A
    p_find = patch(
        "app.services.distributor_service.DistributorService.find_first_or_raise",
        side_effect=UserNotFoundException,
    )

    with p_find:
        # A / A
        with pytest.raises(UserNotFoundException):
            DistributorService.deactivate(999)


def test_deactivate__toggles_each_seller_staged(mock_user: MagicMock):
    # A
    seller1, seller2 = MagicMock(), MagicMock()
    mock_user.sellers = [seller1, seller2]

    p_find = patch(
        "app.services.distributor_service.DistributorService.find_first_or_raise",
        return_value=mock_user,
    )
    p_toggle_staged = patch(
        "app.services.distributor_service.User.toggle_activation_staged"
    )
    p_toggle = patch("app.services.distributor_service.User.toggle_activation")
    p_db = patch("app.services.distributor_service.db")

    with p_find, p_toggle_staged as mock_toggle_staged, p_toggle, p_db:
        # A
        DistributorService.deactivate(mock_user.id)

        # A
        mock_toggle_staged.assert_any_call(seller1)
        mock_toggle_staged.assert_any_call(seller2)


def test_deactivate__toggles_distributor_activation(mock_user: MagicMock):
    # A
    mock_user.sellers = []

    p_find = patch(
        "app.services.distributor_service.DistributorService.find_first_or_raise",
        return_value=mock_user,
    )
    p_toggle_staged = patch(
        "app.services.distributor_service.User.toggle_activation_staged"
    )
    p_toggle = patch("app.services.distributor_service.User.toggle_activation")
    p_db = patch("app.services.distributor_service.db")

    with p_find, p_toggle_staged, p_toggle as mock_toggle, p_db:
        # A
        DistributorService.deactivate(mock_user.id)

        # A
        mock_toggle.assert_called_once_with(mock_user)
