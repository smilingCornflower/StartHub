from application.builders.domain_service.permission import PermissionServiceBuilder
from application.ports.domain_service_builder import AbstractDomainServiceBuilder
from domain.services.notification import NotificationService
from infrastructure.repositories.notification import DjNotificationReadRepository, DjNotificationWriteRepository


class NotificationServiceBuilder(AbstractDomainServiceBuilder[NotificationService]):
    @staticmethod
    def create_service() -> NotificationService:
        return NotificationService(
            permission_service=PermissionServiceBuilder.create_service(),
            read_repository=DjNotificationReadRepository(),
            write_repository=DjNotificationWriteRepository(),
        )
