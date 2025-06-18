from application.ports.domain_service_factory import AbstractDomainServiceFactory
from domain.services.permission import PermissionService
from infrastructure.repositories.permission import DjPermissionReadRepository
from infrastructure.repositories.user import DjUserReadRepository


class PermissionServiceFactory(AbstractDomainServiceFactory[PermissionService]):
    @staticmethod
    def create_service() -> PermissionService:
        return PermissionService(
            user_read_repository=DjUserReadRepository(),
            permission_read_repository=DjPermissionReadRepository(),
        )
