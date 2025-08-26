from domain.enums.permission import ActionEnum, ScopeEnum
from domain.exceptions.permissions import ViewDeniedPermissionException
from domain.models.user_management.message import UserMessage
from domain.models.user_management.user import User
from domain.ports.service import AbstractDomainService
from domain.repositories.user_management.user_message import UserMessageWriteRepository
from domain.services.permission import PermissionService
from domain.value_objects.user_management.user_message import UserMessageCreatePayload
from loguru import logger


class UserMessagePermissionService(AbstractDomainService):
    def __init__(self, permission_service: PermissionService):
        self._permission_service = permission_service

    def check_permission_to_view_any_messages(self, user: User) -> None:
        """:raises ViewDeniedPermissionException:"""
        if self._permission_service.is_allowed_for_user(
            user=user, model=UserMessage, action=ActionEnum.VIEW, scope=ScopeEnum.ANY
        ):
            return None
        raise ViewDeniedPermissionException("You don't have enough permissions to view this resource.")


class UserMessageService(UserMessagePermissionService):
    def __init__(
        self,
        permission_service: PermissionService,
        write_repository: UserMessageWriteRepository,
    ):
        super().__init__(permission_service=permission_service)
        self._write_repository = write_repository

    def create(self, payload: UserMessageCreatePayload) -> None:
        self._write_repository.create(data=payload)
        logger.info("User message was created successfully.")
