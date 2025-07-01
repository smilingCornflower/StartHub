from typing import cast

from application.dto.auth import AccessPayloadDto
from application.service_factories.app_service.auth import AuthAppServiceFactory
from application.services.auth import AuthAppService
from application.services.gateway import gateway
from django.http import HttpHeaders


def get_access_payload_dto(cookies: dict[str, str]) -> AccessPayloadDto:
    """
    :raises MissingAccessTokenException:
    :raises InvalidTokenException:
    :raises TokenExpiredException:
    """
    auth_service: AuthAppService = AuthAppServiceFactory.create_service()
    return auth_service.verify_access(cookies)


def get_access_payload_dto_from_headers(headers: HttpHeaders) -> AccessPayloadDto:
    """
    :raises MissingRequiredFieldException:
    :raises InvalidTokenException:
    :raises TokenExpiredException:
    """
    return gateway.auth_app_service.verify_access_from_headers(headers=cast(dict[str, str], headers))
