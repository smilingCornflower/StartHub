from django.http import QueryDict
from domain.exceptions.validation import ValidationException
from domain.value_objects.auth import LoginCredentials
from domain.value_objects.payload import UserCreatePayload
from domain.value_objects.token import AccessTokenVo, RefreshTokenVo
from domain.value_objects.user import Email, RawPassword, Username
from loguru import logger


def request_data_to_user_create_payload(data: QueryDict) -> UserCreatePayload:
    """
    :raises ValidationException: If required fields missing or Email / Username / RawPassword validation fails.
    """
    username: str | None = data.get("username")
    email: str | None = data.get("email")
    password: str | None = data.get("password")

    logger.debug(f"username = {username}")
    logger.debug(f"email = {email}")
    logger.debug(f"Is password provided = {bool(password)}")

    if not (username and email and password):
        logger.error("Missing required fields.")
        raise ValidationException("Missing required fields: username, email or password.")

    return UserCreatePayload(username=Username(username), email=Email(email), password=RawPassword(password))


def request_data_to_login_credentials(data: QueryDict) -> LoginCredentials:
    """
    Convert request data to LoginCredentials.

    :raises ValidationException: If required fields missing or Email / RawPassword validation fails.
    """
    email: str | None = data.get("email")
    password: str | None = data.get("password")

    logger.debug(f"email = {email}")
    logger.debug(f"Is password provided = {bool(password)}")

    if not (email and password):
        logger.error("Missing required fields.")
        raise ValidationException("Missing required fields: email or password.")

    return LoginCredentials(email=Email(email), password=RawPassword(password))


def request_cookies_to_refresh_token(cookies: dict[str, str]) -> RefreshTokenVo:
    """:raises ValidationException: If missing 'refresh_token' field."""
    token: str | None = cookies.get("refresh_token")

    if not token:
        logger.error("Missing refresh_token field.")
        raise ValidationException("Missing required field: refresh_token.")
    return RefreshTokenVo(value=token)


def request_cookies_to_access_token(cookies: dict[str, str]) -> AccessTokenVo:
    """:raises ValidationException: If missing 'access_token' field."""
    token: str | None = cookies.get("access_token")
    if not token:
        logger.error("Missing access_token field.")
        raise ValidationException("Missing required field: access_token.")
    return AccessTokenVo(value=token)
