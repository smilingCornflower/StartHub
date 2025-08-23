from typing import cast

from django.http import HttpHeaders
from loguru import logger

from application.dto.auth import AccessPayloadDto, AnonymousPayloadDto
from application.services.gateway import gateway


def get_access_payload_dto_from_headers(headers: HttpHeaders) -> AccessPayloadDto:
    """
    :raises MissingRequiredFieldException:
    :raises InvalidTokenException:
    :raises TokenExpiredException:
    :raises pydantic.ValidationError:
    It also can raise InvalidTokenException if the token type is not access.
    """
    return gateway.auth_app_service.verify_access_from_headers(headers=cast(dict[str, str], headers))


def get_anonymous_payload_dto_from_headers(headers: HttpHeaders) -> AnonymousPayloadDto:
    """
    :raises MissingRequiredFieldException:
    :raises InvalidTokenException:
    :raises TokenExpiredException:
    :raises pydantic.ValidationError:
    It also can raise InvalidTokenException if the token type is not anonymous.
    """
    return gateway.auth_app_service.verify_anonymous_from_headers(headers=cast(dict[str, str], headers))


def get_access_or_anonymous_payload_dto_from_headers(headers: HttpHeaders) -> AccessPayloadDto | AnonymousPayloadDto:
    """
    :raises MissingRequiredFieldException:
    :raises InvalidTokenException:
    :raises TokenExpiredException:
    :raises pydantic.ValidationError:
    """
    token = gateway.auth_app_service.verify_access_or_anonymous_from_headers(headers=cast(dict[str, str], headers))
    logger.info(f"Received token type = {type(token)}")
    return token
