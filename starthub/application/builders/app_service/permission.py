from application.builders.domain_service.permission import PermissionServiceBuilder
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.user_management.permission import PermissionAppService
from infrastructure.repositories.permission import DjPermissionReadRepository
from infrastructure.repositories.user_management.user import DjUserReadRepository


class PermissionAppServiceBuilder(AbstractAppServiceBuilder[PermissionAppService]):
    @staticmethod
    def create_service() -> PermissionAppService:
        return PermissionAppService(
            permission_service=PermissionServiceBuilder.create_service(),
            permission_read_reposiotory=DjPermissionReadRepository(),
            user_read_repository=DjUserReadRepository(),
        )
