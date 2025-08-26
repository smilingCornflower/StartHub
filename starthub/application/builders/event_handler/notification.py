from typing import Any

from application.builders.domain_service.notification import NotificationServiceBuilder
from application.event_handlers.notifications.project import (
    ProjectApprovedNotificationEventHandler,
    ProjectRejectedNotificationEventHandler,
)
from application.ports.event_handler_builder import AbstractEventHandlerBuilder


class ProjectRejectedNotificationEventHandlerBuilder(AbstractEventHandlerBuilder[Any]):
    @staticmethod
    def create_handler() -> ProjectRejectedNotificationEventHandler:
        return ProjectRejectedNotificationEventHandler(
            notification_service=NotificationServiceBuilder.create_service(),
        )


class ProjectApprovedNotificationEventHandlerBuilder(AbstractEventHandlerBuilder[Any]):
    @staticmethod
    def create_handler() -> ProjectApprovedNotificationEventHandler:
        return ProjectApprovedNotificationEventHandler(
            notification_service=NotificationServiceBuilder.create_service(),
        )
