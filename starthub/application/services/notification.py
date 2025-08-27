from application.dto.notification import NotificationDto
from application.ports.service import AbstractAppService
from domain.models.notification import Notification
from domain.repositories.notification import NotificationReadRepository
from domain.repositories.user_management.user import UserReadRepository
from domain.services.notification import NotificationService
from domain.value_objects.common import CursorPagination, Id
from domain.value_objects.filter import NotificationFilter
from domain.value_objects.notification import NotificationGetCommand
from loguru import logger


class NotificationAppService(AbstractAppService):
    def __init__(
        self,
        notification_service: NotificationService,
        notification_read_repository: NotificationReadRepository,
        user_read_repositroy: UserReadRepository,
    ):
        self._notification_service = notification_service
        self._notification_read_repository = notification_read_repository
        self._user_read_repositroy = user_read_repositroy

    def get_all(
        self, caller_user_id: Id, target_user_id: Id, command: NotificationGetCommand, pagniation: CursorPagination
    ) -> list[NotificationDto]:
        """
        :raises ViewDeniedPermissionException:
        :raises UserNotFoundException:
        """

        caller_user = self._user_read_repositroy.get_by_id(id_=caller_user_id)
        target_user = self._user_read_repositroy.get_by_id(id_=target_user_id)

        self._notification_service.check_can_user_read_notification(caller_user=caller_user, target_user=target_user)
        filter_ = NotificationFilter(user_id=target_user_id, is_read=command.is_read)
        notifications: list[Notification] = self._notification_read_repository.get_all(
            filter_=filter_, pagination=pagniation
        )
        logger.debug(f"Found {len(notifications)} notifications.")

        result = [self._create_dto(notification) for notification in notifications]
        self._notification_service.mark_as_read(notifications=notifications)
        return result

    def _create_dto(self, notification: Notification) -> NotificationDto:
        return NotificationDto(title=notification.title, message=notification.message, is_read=notification.is_read)
