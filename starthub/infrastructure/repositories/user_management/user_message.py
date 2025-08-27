from domain.exceptions.user_message import UserMessageNotFoundException
from domain.models.user_management.message import UserMessage
from domain.repositories.user_management.user_message import UserMessageReadRepository, UserMessageWriteRepository
from domain.value_objects.common import CursorPagination, OffsetPagination
from domain.value_objects.filter import UserMessageFilter
from domain.value_objects.user_management.user_message import (
    UserMessageCreatePayload,
    UserMessageId,
    UserMessageUpdatePayload,
)
from infrastructure.repositories.pagination import apply_pagination
from loguru import logger


class DjUserMessageReadRepository(UserMessageReadRepository):
    def get_by_id(self, id_: UserMessageId) -> UserMessage:
        """:raises UserMessageNotFoundException:"""
        user_message: UserMessage | None = UserMessage.objects.filter(id=id_.value).first()
        if user_message is None:
            raise UserMessageNotFoundException(f"User message with id = {id_.value} not found.")
        return user_message

    def get_all(
        self, filter_: UserMessageFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[UserMessage]:
        queryset = UserMessage.objects.all()

        if filter_.user_id is not None:
            queryset = queryset.filter(user_id=filter_.user_id.value)
        if filter_.is_read is not None:
            queryset = queryset.filter(is_read=filter_.is_read)

        if filter_.order_by is not None:
            queryset = queryset.order_by(filter_.order_by)

        if pagination is not None:
            return apply_pagination(queryset=queryset, pagination=pagination)

        return list(queryset)


class DjUserMessageWriteRepository(UserMessageWriteRepository):
    def create(self, data: UserMessageCreatePayload) -> UserMessage:
        return UserMessage.objects.create(
            user_id=data.user_id.value,
            first_name=data.first_name.value,
            last_name=data.last_name.value,
            email=data.email.value,
            phone=data.phone.value,
            topic=data.topic.value,
            content=data.content.value,
        )

    def update(self, data: UserMessageUpdatePayload) -> UserMessage:
        raise NotImplementedError("the method update() is not implemented yet.")

    def delete_by_id(self, id_: UserMessageId) -> None:
        """:raises UserMessageNotFoundException:"""
        try:
            UserMessage.objects.get(id=id_.value).delete()
        except UserMessage.DoesNotExist:
            logger.exception(f"UserMessage with id = {id_.value} doesn't exist.")
            raise UserMessageNotFoundException(f"User message with id = {id_.value} not found.")

    def delete(self, message: UserMessage) -> None:
        message.delete()
