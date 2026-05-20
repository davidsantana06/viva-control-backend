from unittest.mock import patch, MagicMock
import pytest

from app.services import SelfService
from app.exceptions import UserNotFoundException


def test_find_first_or_raise__returns_user(mock_user: MagicMock):
    # A
    p_find = patch(
        "app.services.self_service.User.find_first_by_id",
        return_value=mock_user,
    )

    with p_find:
        # A
        result = SelfService.find_first_or_raise(mock_user.id)

        # A
        assert result == mock_user


def test_find_first_or_raise__raises_if_not_found():
    # A
    p_find = patch(
        "app.services.self_service.User.find_first_by_id",
        return_value=None,
    )

    with p_find:
        # A / A
        with pytest.raises(UserNotFoundException):
            SelfService.find_first_or_raise(999)


def test_update__returns_updated_user(mock_user: MagicMock):
    # A
    p_find = patch(
        "app.services.self_service.SelfService.find_first_or_raise",
        return_value=mock_user,
    )
    p_save = patch("app.services.self_service.User.save")

    with p_find, p_save:
        # A
        result = SelfService.update(mock_user.id, {"name": "David"})

        # A
        assert result == mock_user


def test_update__hashes_password_if_provided(mock_user: MagicMock):
    # A
    p_find = patch(
        "app.services.self_service.SelfService.find_first_or_raise",
        return_value=mock_user,
    )
    p_hash = patch(
        "app.services.self_service.Security.hash_password",
        return_value="hashed",
    )
    p_save = patch("app.services.self_service.User.save")

    with p_find, p_hash as mock_hash, p_save:
        # A
        SelfService.update(mock_user.id, {"password": "nova"})

        # A
        mock_hash.assert_called_once_with("nova")


def test_update__does_not_hash_password_if_not_provided(mock_user: MagicMock):
    # A
    p_find = patch(
        "app.services.self_service.SelfService.find_first_or_raise",
        return_value=mock_user,
    )
    p_hash = patch("app.services.self_service.Security.hash_password")
    p_save = patch("app.services.self_service.User.save")

    with p_find, p_hash as mock_hash, p_save:
        # A
        SelfService.update(mock_user.id, {"name": "David"})

        # A
        mock_hash.assert_not_called()
