# from loguru import logger
#
# from domain.events.project import ProjectRejectedEvent
# from domain.ports.event import AbstractEventHandler
# from domain.services.notification import NotificationService
# from domain.value_objects.notification import NotificationCreatePayload, NotificationTitle, NotificationMessage
#
#
# class ProjectRejectedEventHandler(AbstractEventHandler[ProjectRejectedEvent]):
#     def __init__(self, notification_service: NotificationService):
#         self._notification_service = notification_service
#
#     def handle(self, event: ProjectRejectedEvent) -> None:
#         create_payload = NotificationCreatePayload(
#             user_id=event.user_id,
#             title=NotificationTitle(value="Your project submission was rejected"),
#             message=NotificationMessage(value=event.report.value),
#         )
#         self._notification_service.create(payload=create_payload)
#         logger.info("Notfication send successfully.")
