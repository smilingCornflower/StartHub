from typing import cast

from django.http import HttpHeaders

from application.dto.auth import AccessPayloadDto, AnonymousPayloadDto
from application.services.gateway import gateway


def get_access_payload_dto_from_headers(headers: HttpHeaders) -> AccessPayloadDto:
    """
    :raises MissingRequiredFieldException:
    :raises InvalidTokenException:
    :raises TokenExpiredException:
    """
    return gateway.auth_app_service.verify_access_from_headers(headers=cast(dict[str, str], headers))


def get_anonymous_payload_dto_from_headers(headers: HttpHeaders) -> AnonymousPayloadDto:
    """
    :raises MissingRequiredFieldException:
    :raises InvalidTokenException:
    :raises TokenExpiredException:
    """
    return gateway.auth_app_service.verify_anonymous_from_headers(headers=cast(dict[str, str], headers))
