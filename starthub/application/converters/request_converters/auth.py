from domain.exceptions.auth import MissingAccessTokenException
from domain.exceptions.validation import MissingRequiredFieldException, ValidationException
from domain.value_objects.auth import LoginCredentials
from domain.value_objects.common import FirstName, LastName
from domain.value_objects.token import AccessTokenVo, RefreshTokenVo
from domain.value_objects.user import Email, RawPassword, UserCreatePayload
from loguru import logger


def request_data_to_user_create_payload(data: dict[str, str]) -> UserCreatePayload:
    """
    :raises MissingRequiredFieldException:
    :raises FirstNameIsTooLongException:
    :raises LastNameIsTooLongException:
    :raises EmptyStringException:
    :raises InvalidEmailException:
    :raises PasswordValidationException:
    :raises pydantic.ValidationError: If fields has incorrect types
    """
    first_name: str | None = data.get("first_name")
    last_name: str | None = data.get("last_name")
    email: str | None = data.get("email")
    password: str | None = data.get("password")

    logger.debug(f"first_name = {first_name}")
    logger.debug(f"last_name = {last_name}")
    logger.debug(f"email = {email}")
    logger.debug(f"Is password provided = {bool(password)}")

    if first_name is None or last_name is None or email is None or password is None:
        logger.error("Missing required fields.")
        raise MissingRequiredFieldException("Missing required fields: first_name, last_name, email or password.")

    return UserCreatePayload(
        first_name=FirstName(value=first_name),
        last_name=LastName(value=last_name),
        email=Email(value=email),
        password=RawPassword(value=password),
    )


def request_data_to_login_credentials(data: dict[str, str]) -> LoginCredentials:
    """
    :raises MissingRequiredFieldException:
    :raises EmptyStringException:
    :raises InvalidEmailException:
    :raises PasswordValidationException:
    :raises pydantic.ValidationError: If fields has incorrect types
    """
    email: str | None = data.get("email")
    password: str | None = data.get("password")

    logger.debug(f"email = {email}")
    logger.debug(f"Is password provided = {bool(password)}")

    if email is None or password is None:
        logger.error("Missing required fields.")
        raise MissingRequiredFieldException("Missing required fields: email or password.")

    return LoginCredentials(email=Email(value=email), password=RawPassword(value=password))


def request_cookies_to_refresh_token(cookies: dict[str, str]) -> RefreshTokenVo:
    """:raises ValidationException: If missing 'refresh_token' field."""
    token: str | None = cookies.get("refresh_token")

    if not token:
        logger.error("Missing refresh_token field.")
        raise ValidationException("Missing required field: refresh_token.")
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
