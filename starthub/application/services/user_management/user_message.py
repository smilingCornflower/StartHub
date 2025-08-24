from application.dto.user import UserMessageDto
from application.ports.service import AbstractAppService
from domain.constants import USER_UNREAD_MESSAGES_MAX_AMOUNT
from domain.exceptions.user_message import UserUnreadMessageMaxAmountException
from domain.models.user_management.message import UserMessage
from domain.repositories.user_management.user import UserReadRepository
from domain.repositories.user_management.user_message import UserMessageReadRepository
from domain.services.users_management.user_message import UserMessageService
from domain.value_objects.common import Id, Pagination
from domain.value_objects.filter import UserMessageFilter
from domain.value_objects.user_management.user_message import (
    UserMessageCreateCommand,
    UserMessageCreatePayload,
    UserMessageGetCommand,
)


class UserMessageAppService(AbstractAppService):
    def __init__(
        self,
        user_message_service: UserMessageService,
        user_read_repository: UserReadRepository,
        user_message_read_repository: UserMessageReadRepository,
    ):
        self._user_message_service = user_message_service
        self._user_read_repository = user_read_repository
        self._user_message_read_repository = user_message_read_repository

    def get(self, user_id: Id, pagination: Pagination, command: UserMessageGetCommand) -> list[UserMessageDto]:
        user = self._user_read_repository.get_by_id(id_=user_id)
        self._user_message_service.check_permission_to_view_any_messages(user=user)

        message_filter = UserMessageFilter(is_read=command.is_read, order_by=command.order_by)
        messages = self._user_message_read_repository.get_all(filter_=message_filter, pagination=pagination)

        return [self._create_dto(message=i) for i in messages]

    def get_my(self, user_id: Id, pagination: Pagination, command: UserMessageGetCommand) -> list[UserMessageDto]:
        message_filter = UserMessageFilter(user_id=user_id, is_read=command.is_read, order_by=command.order_by)
        messages = self._user_message_read_repository.get_all(filter_=message_filter, pagination=pagination)

        return [self._create_dto(message=i) for i in messages]

    def _create_dto(self, message: UserMessage) -> UserMessageDto:
        return UserMessageDto(
            id=message.id,
            user_id=message.user_id,
            first_name=message.first_name,
            last_name=message.last_name,
            email=message.email,
            topic=message.topic,
            content=message.content,
            created_at=message.created_at,
        )

    def create(self, user_id: Id, command: UserMessageCreateCommand) -> None:
        self._user_read_repository.get_by_id(id_=user_id)
        self._check_unread_messages_max_amount(user_id=user_id)

        payload = self._convert_create_command_to_payload(user_id=user_id, command=command)
        self._user_message_service.create(payload=payload)

        return None

    def _convert_create_command_to_payload(
        self, user_id: Id, command: UserMessageCreateCommand
    ) -> UserMessageCreatePayload:
        return UserMessageCreatePayload(
            user_id=user_id,
            first_name=command.first_name,
            last_name=command.last_name,
            email=command.email,
            phone=command.phone,
            topic=command.topic,
            content=command.content,
        )

    def _check_unread_messages_max_amount(self, user_id: Id) -> None:
        """:raises UserUnreadMessageMaxAmountException:"""
        messages: list[UserMessage] = self._user_message_read_repository.get_all(
            filter_=UserMessageFilter(user_id=user_id, is_read=False)
        )
        if not (len(messages) < USER_UNREAD_MESSAGES_MAX_AMOUNT):
            raise UserUnreadMessageMaxAmountException(
                f"You have reached the maximum number of unread messages ({USER_UNREAD_MESSAGES_MAX_AMOUNT})."
            )

        return None
