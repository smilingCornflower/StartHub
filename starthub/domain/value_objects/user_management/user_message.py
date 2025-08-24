from domain.constants import USER_MESSAGE_CONTENT_MAX_LENGTH
from domain.ports.command import BaseCommand
from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects.common import FirstName, Id, LastName, LongString, PhoneNumber, StringVo
from domain.value_objects.user_management.user import Email


class UserMessageId(Id):
    pass


class UserMessageTopic(LongString):
    pass


class UserMessageContent(StringVo):
    max_length = USER_MESSAGE_CONTENT_MAX_LENGTH


class UserMessageCreatePayload(AbstractCreatePayload):
    user_id: Id
    first_name: FirstName
    last_name: LastName
    email: Email
    phone: PhoneNumber
    topic: UserMessageTopic
    content: UserMessageContent


class UserMessageUpdatePayload(AbstractUpdatePayload):
    pass


class UserMessageCreateCommand(BaseCommand):
    pass
