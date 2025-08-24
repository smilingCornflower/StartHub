from application.ports.domain_service_builder import AbstractDomainServiceBuilder
from domain.services.notification import NotificationService
from infrastructure.repositories.notification import DjNotificationReadRepository, DjNotificationWriteRepository


class NotificationServiceBuilder(AbstractDomainServiceBuilder[NotificationService]):
    @staticmethod
    def create_service() -> NotificationService:
        return NotificationService(
            read_repository=DjNotificationReadRepository(),
            write_repository=DjNotificationWriteRepository(),
        )
