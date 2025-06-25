from application.dto.auth import AccessPayloadDto
from application.service_factories.app_service.auth import AuthAppServiceFactory
from application.services.auth import AuthAppService


def get_access_payload_dto(cookies: dict[str, str]) -> AccessPayloadDto:
    """
    :raises MissingAccessTokenException:
    :raises InvalidTokenException:
    :raises TokenExpiredException:
    """
    auth_service: AuthAppService = AuthAppServiceFactory.create_service()
    return auth_service.verify_access(cookies)
