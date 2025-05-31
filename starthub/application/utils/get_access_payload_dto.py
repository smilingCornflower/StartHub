from application.dto.auth import AccessPayloadDto
from application.service_factories.auth import AuthServiceFactory
from application.services.auth import AuthAppService


def get_access_payload_dto(cookies: dict[str, str]) -> AccessPayloadDto:
    """
    :raises ValidationException:
    :raises InvalidTokenException:
    """
    auth_service: AuthAppService = AuthServiceFactory.create_service()
    return auth_service.verify_access(cookies)
