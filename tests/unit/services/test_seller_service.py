from unittest.mock import patch, MagicMock
import pytest

from app.services import SellerService
from app.exceptions import EmailAlreadyRegisteredException, UserNotFoundException
from app.types import UserRole


def test_find_first__returns_seller(mock_user: MagicMock):
    # A
    p_find = patch(
        "app.services.seller_service.User.find_first_by_id_and_role",
        return_value=mock_user,
    )

    with p_find:
        # A
        result = SellerService.find_first(mock_user.id)

        # A
        assert result == mock_user


def test_find_first__returns_none_if_not_found():
    # A
    p_find = patch(
        "app.services.seller_service.User.find_first_by_id_and_role",
        return_value=None,
    )

    with p_find:
        # A
        result = SellerService.find_first(999)

        # A
        assert result is None


def test_find_first_or_raise__returns_seller(mock_user: MagicMock):
    # A
    p_find = patch(
        "app.services.seller_service.SellerService.find_first",
        return_value=mock_user,
    )

    with p_find:
        # A
        result = SellerService.find_first_or_raise(mock_user.id)

        # A
        assert result == mock_user


def test_find_first_or_raise__raises_if_not_found():
    # A
    p_find = patch(
        "app.services.seller_service.SellerService.find_first",
        return_value=None,
    )

    with p_find:
        # A / A
        with pytest.raises(UserNotFoundException):
            SellerService.find_first_or_raise(999)


def test_find_all__returns_list(mock_user: MagicMock):
    # A
    params = MagicMock()
    p_find = patch(
        "app.services.seller_service.User.find_all_by_role",
        return_value=[mock_user],
    )

    with p_find as mock_find_all:
        # A
        result = SellerService.find_all(params)

        # A
        assert result == [mock_user]
        mock_find_all.assert_called_once_with(params, {}, role=UserRole.SELLER)


def test_activate__raises_if_seller_not_found():
    # A
    p_find = patch(
        "app.services.seller_service.SellerService.find_first_or_raise",
        side_effect=UserNotFoundException,
    )

    with p_find:
        # A / A
        with pytest.raises(UserNotFoundException):
            SellerService.activate(999)


def test_activate__toggles_seller_activation(mock_user: MagicMock):
    # A
    p_find = patch(
        "app.services.seller_service.SellerService.find_first_or_raise",
        return_value=mock_user,
    )
    p_toggle = patch("app.services.seller_service.User.toggle_activation")

    with p_find, p_toggle as mock_toggle:
        # A
        SellerService.activate(mock_user.id)

        # A
        mock_toggle.assert_called_once_with(mock_user)


def test_deactivate__raises_if_seller_not_found():
    # A
    p_find = patch(
        "app.services.seller_service.SellerService.find_first_or_raise",
        side_effect=UserNotFoundException,
    )

    with p_find:
        # A / A
        with pytest.raises(UserNotFoundException):
            SellerService.deactivate(999)


def test_deactivate__toggles_seller_activation(mock_user: MagicMock):
    # A
    p_find = patch(
        "app.services.seller_service.SellerService.find_first_or_raise",
        return_value=mock_user,
    )
    p_toggle = patch("app.services.seller_service.User.toggle_activation")

    with p_find, p_toggle as mock_toggle:
        # A
        SellerService.deactivate(mock_user.id)

        # A
        mock_toggle.assert_called_once_with(mock_user)


# -- create / update inherited from UserService --


def test_create__returns_created_user(mock_user: MagicMock):
    # A
    p_user_cls = patch("app.services.base.user_service.User")
    p_hash = patch(
        "app.services.base.user_service.Security.hash_password",
        return_value="hashed",
    )

    with p_user_cls as MockUser, p_hash:
        MockUser.find_first_by_email.return_value = None
        MockUser.return_value = mock_user

        # A
        result = SellerService.create(
            {
                "email": "a@a.com",
                "password": "senha123",
                "name": "Test",
                "role": "SELLER",
            }
        )

        # A
        assert result == mock_user


def test_create__hashes_password(mock_user: MagicMock):
    # A
    p_user_cls = patch("app.services.base.user_service.User")
    p_hash = patch(
        "app.services.base.user_service.Security.hash_password",
        return_value="hashed",
    )

    with p_user_cls as MockUser, p_hash as mock_hash:
        MockUser.find_first_by_email.return_value = None
        MockUser.return_value = mock_user

        # A
        SellerService.create(
            {
                "email": "a@a.com",
                "password": "senha123",
                "name": "Test",
                "role": "SELLER",
            }
        )

        # A
        mock_hash.assert_called_once_with("senha123")


def test_create__raises_if_email_already_registered(mock_user: MagicMock):
    # A
    p_find = patch(
        "app.services.base.user_service.User.find_first_by_email",
        return_value=mock_user,
    )

    with p_find:
        # A / A
        with pytest.raises(EmailAlreadyRegisteredException):
            SellerService.create(
                {
                    "email": "a@a.com",
                    "password": "senha123",
                    "name": "Test",
                    "role": "SELLER",
                }
            )


def test_update__returns_updated_user(mock_user: MagicMock):
    # A
    p_find = patch(
        "app.services.seller_service.SellerService.find_first_or_raise",
        return_value=mock_user,
    )
    p_save = patch("app.services.base.user_service.User.save")

    with p_find, p_save:
        # A
        result = SellerService.update(mock_user.id, {"name": "David"})

        # A
        assert result == mock_user


def test_update__hashes_password_if_provided(mock_user: MagicMock):
    # A
    p_find = patch(
        "app.services.seller_service.SellerService.find_first_or_raise",
        return_value=mock_user,
    )
    p_hash = patch(
        "app.services.base.user_service.Security.hash_password",
        return_value="hashed",
    )
    p_save = patch("app.services.base.user_service.User.save")

    with p_find, p_hash as mock_hash, p_save:
        # A
        SellerService.update(mock_user.id, {"password": "nova"})

        # A
        mock_hash.assert_called_once_with("nova")


def test_update__does_not_hash_password_if_not_provided(mock_user: MagicMock):
    # A
    p_find = patch(
        "app.services.seller_service.SellerService.find_first_or_raise",
        return_value=mock_user,
    )
    p_hash = patch("app.services.base.user_service.Security.hash_password")
    p_save = patch("app.services.base.user_service.User.save")

    with p_find, p_hash as mock_hash, p_save:
        # A
        SellerService.update(mock_user.id, {"name": "David"})

        # A
        mock_hash.assert_not_called()
