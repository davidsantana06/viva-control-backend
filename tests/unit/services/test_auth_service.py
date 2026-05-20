from unittest.mock import patch, MagicMock
import pytest
from app.services import AuthService
from app.exceptions import InvalidCredentialsException, UserNotFoundException


def test_issue_token_pair__returns_token_pair(mock_user: MagicMock):
    # Arrange
    p_find = patch(
        "app.services.auth_service.User.find_first_by_email",
        return_value=mock_user,
    )
    p_verify = patch(
        "app.services.auth_service.Security.verify_password",
        return_value=True,
    )
    p_access = patch(
        "app.services.auth_service.Security.issue_access_token",
        return_value="access",
    )
    p_refresh = patch(
        "app.services.auth_service.Security.issue_refresh_token",
        return_value="refresh",
    )

    with p_find, p_verify, p_access, p_refresh:
        # Act
        result = AuthService.issue_token_pair(
            {"email": "a@a.com", "password": "senha123"}
        )

        # Assert
        assert result["access_token"] == "access"
        assert result["refresh_token"] == "refresh"


def test_issue_token_pair__raises_if_user_not_found():
    # A
    p_find = patch(
        "app.services.auth_service.User.find_first_by_email",
        return_value=None,
    )

    with p_find:
        # A / A
        with pytest.raises(InvalidCredentialsException):
            AuthService.issue_token_pair(
                {"email": "naoexiste@a.com", "password": "senha123"}
            )


def test_issue_token_pair__raises_if_password_is_wrong(mock_user: MagicMock):
    # A
    p_find = patch(
        "app.services.auth_service.User.find_first_by_email",
        return_value=mock_user,
    )
    p_verify = patch(
        "app.services.auth_service.Security.verify_password",
        return_value=False,
    )

    with p_find, p_verify:
        # A / A
        with pytest.raises(InvalidCredentialsException):
            AuthService.issue_token_pair({"email": "a@a.com", "password": "errada"})


def test_refresh_access_token__returns_new_access_token(mock_user: MagicMock):
    # A
    p_find = patch(
        "app.services.auth_service.User.find_first_by_id",
        return_value=mock_user,
    )
    p_access = patch(
        "app.services.auth_service.Security.issue_access_token",
        return_value="new_access",
    )

    with p_find, p_access:
        # A
        result = AuthService.refresh_access_token(mock_user.id)

        # A
        assert result["access_token"] == "new_access"


def test_refresh_access_token__raises_if_user_not_found():
    # A
    p_find = patch(
        "app.services.auth_service.User.find_first_by_id",
        return_value=None,
    )

    with p_find:
        # A / A
        with pytest.raises(UserNotFoundException):
            AuthService.refresh_access_token(999)
