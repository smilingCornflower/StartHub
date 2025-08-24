from domain.exceptions.permissions import ViewDeniedPermissionException
from domain.models.notification import Notification
from domain.models.user import User
from domain.ports.service import AbstractDomainService
from domain.repositories.notification import NotificationReadRepository, NotificationWriteRepository
from domain.services.permission import PermissionService
from domain.value_objects.notification import NotificationCreatePayload


class NotificationPermissionService(AbstractDomainService):
    def __init__(self, permission_service: PermissionService):
        self._permission_servcie = permission_service

    def check_can_user_read_notification(self, caller_user: User, target_user: User) -> None:
        """:raises ViewDeniedPermissionException:"""
        if caller_user == target_user:
            return None
        raise ViewDeniedPermissionException(f"You cannot read notifications for the user with id = {target_user.id}.")


class NotificationService(NotificationPermissionService):
    def __init__(
        self,
        permission_service: PermissionService,
        read_repository: NotificationReadRepository,
        write_repository: NotificationWriteRepository,
    ):
        super().__init__(permission_service=permission_service)
        self._read_repository = read_repository
        self._write_repository = write_repository

    def create(self, payload: NotificationCreatePayload) -> Notification:
        return self._write_repository.create(data=payload)

    def mark_as_read(self, notifications: list[Notification]) -> None:
        for notification in notifications:
            self._write_repository.mark_as_read(notification=notification)
