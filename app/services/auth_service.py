from app.dtos import AccessTokenDto, LoginDto, TokenPairDto
from app.exceptions import InvalidCredentialsException, UserNotFoundException
from app.facades import Security
from app.models import User


class AuthService:
    @staticmethod
    def issue_token_pair(dto: LoginDto) -> TokenPairDto:
        user = User.find_first_by_email(dto["email"])

        invalid_credentials = not user or not Security.verify_password(
            user.password_hash,
            dto["password"],
        )
        if invalid_credentials:
            raise InvalidCredentialsException()

        return TokenPairDto(
            access_token=Security.issue_access_token(user),
            refresh_token=Security.issue_refresh_token(user),
        )

    @staticmethod
    def refresh_access_token(identity: int) -> AccessTokenDto:
        user = User.find_first_by_id(identity)

        if not user:
            raise UserNotFoundException()

        return AccessTokenDto(
            access_token=Security.issue_access_token(user),
        )
