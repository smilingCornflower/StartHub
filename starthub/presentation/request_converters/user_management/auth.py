import re

import jwt
from domain.enums.token import TokenTypeEnum
from domain.exceptions.auth import MissingAccessTokenException
from domain.exceptions.validation import MissingRequiredFieldException
from domain.value_objects.auth_management.auth import LoginCredentials
from domain.value_objects.auth_management.token import AccessTokenVo, AnonymousTokenVo, RefreshTokenVo
from domain.value_objects.user_management.user import Email, RawPassword, UserCreatePayload
from loguru import logger
from presentation.request_converters.common import get_required_field


def request_data_to_user_create_payload(data: dict[str, str]) -> UserCreatePayload:
    """:raises MissingRequiredFieldException:"""
    email: str | None = data.get("email")
    password: str | None = data.get("password")

    logger.debug(f"email = {email}")
    logger.debug(f"Is password provided = {bool(password)}")

    if email is None or password is None:
        logger.error("Missing required fields.")
        raise MissingRequiredFieldException("Missing required fields: email or password.")

    return UserCreatePayload(
        email=Email(value=email),
        password=RawPassword(value=password),
    )


def request_data_to_login_credentials(data: dict[str, str]) -> LoginCredentials:
    """:raises MissingRequiredFieldException:"""
    email: str | None = data.get("email")
    password: str | None = data.get("password")

    logger.debug(f"email = {email}")
    logger.debug(f"Is password provided = {bool(password)}")

    if email is None or password is None:
        logger.error("Missing required fields.")
        raise MissingRequiredFieldException("Missing required fields: email or password.")

    return LoginCredentials(email=Email(value=email), password=RawPassword(value=password))


def request_cookies_to_refresh_token(cookies: dict[str, str]) -> RefreshTokenVo:
    """:raises MissingRequiredFieldException: If missing 'refresh_token' field."""
    token: str = get_required_field(cookies, "refresh_token")
    return RefreshTokenVo(value=token)


def request_cookies_to_access_token(cookies: dict[str, str]) -> AccessTokenVo:
    """:raises MissingAccessTokenException: If missing 'access_token' field."""
    token: str | None = cookies.get("access_token")
    if not token:
        logger.error("Missing access_token field.")
        raise MissingAccessTokenException("Missing required field: access_token.")
    return AccessTokenVo(value=token)


def request_data_to_email(data: dict[str, str]) -> Email:
    """:raises MissingRequiredFieldException: If missing required fields."""
    try:
        return Email(value=data["email"])
    except KeyError:
        raise MissingRequiredFieldException("Missing required fields: email must be provided.")


def extract_token_from_headers(headers: dict[str, str]) -> str:
    """
    :raises MissingRequiredFieldException:
    """
    auth_header: str = get_required_field(headers, "Authorization")
    bearer_token_regex = r"^Bearer\s(.+)$"
    match: re.Match[str] | None = re.match(bearer_token_regex, auth_header)
    if match:
        token: str = match.group(1)
        return token
    logger.exception("Failed to get Bearer token from Authorization headers.")
    raise MissingRequiredFieldException("Failed to get Bearer token from Authorization headers.")


def request_headers_to_access_token(headers: dict[str, str]) -> AccessTokenVo:
    """
    :raises MissingRequiredFieldException:
    :raises pydantic.ValidationError:
    """
    return AccessTokenVo(value=extract_token_from_headers(headers=headers))


def request_headers_to_anonymous_token(headers: dict[str, str]) -> AnonymousTokenVo:
    """
    :raises MissingRequiredFieldException:
    :raises pydantic.ValidationError:
    """
    return AnonymousTokenVo(value=extract_token_from_headers(headers=headers))


def request_headers_to_access_or_anonymous_token(headers: dict[str, str]) -> AccessTokenVo | AnonymousTokenVo:
    """
    :raises MissingRequiredFieldException:
    :raises pydantic.ValidationError:
    """
    token: str = extract_token_from_headers(headers=headers)
    decoded: dict[str, str] = jwt.decode(token, options={"verify_signature": False})
    logger.debug(f"{decoded=}")

    if get_required_field(decoded, "type", "token['type']") == TokenTypeEnum.ANONYMOUS:
        anonymous_token: str = token.replace("anon:", "")
        return AnonymousTokenVo(value=anonymous_token)
    return AccessTokenVo(value=token)
