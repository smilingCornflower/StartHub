from domain.events.project import ProjectApprovedNotificationEvent, ProjectRejectedNotificationEvent
from domain.ports.event import AbstractEventHandler
from domain.services.notification import NotificationService
from domain.value_objects.notification import NotificationCreatePayload
from loguru import logger


class ProjectRejectedNotificationEventHandler(AbstractEventHandler[ProjectRejectedNotificationEvent]):
    def __init__(self, notification_service: NotificationService):
        self._notification_service = notification_service

    def handle(self, event: ProjectRejectedNotificationEvent) -> None:
        create_payload = NotificationCreatePayload(user_id=event.user_id, title=event.title, message=event.message)
        self._notification_service.create(payload=create_payload)
        logger.info("Notfication send successfully.")


class ProjectApprovedNotificationEventHandler(AbstractEventHandler[ProjectApprovedNotificationEvent]):
    def __init__(self, notification_service: NotificationService):
        self._notification_service = notification_service

    def handle(self, event: ProjectApprovedNotificationEvent) -> None:
        create_payload = NotificationCreatePayload(user_id=event.user_id, title=event.title, message=event.message)
        self._notification_service.create(payload=create_payload)
        logger.info("Notfication send successfully.")
