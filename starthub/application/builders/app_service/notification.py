from application.builders.domain_service.notification import NotificationServiceBuilder
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.notification import NotificationAppService
from infrastructure.repositories.notification import DjNotificationReadRepository
from infrastructure.repositories.user import DjUserReadRepository


class NotificationAppServiceBuilder(AbstractAppServiceBuilder[NotificationAppService]):
    @staticmethod
    def create_service() -> NotificationAppService:
        return NotificationAppService(
            notification_service=NotificationServiceBuilder.create_service(),
            notification_read_repository=DjNotificationReadRepository(),
            user_read_repositroy=DjUserReadRepository(),
        )
