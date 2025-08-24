from domain.constants import NOTIFICATION_MESSAGE_MAX_LENGTH
from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects.common import Id, LongString, StringVo


class NotificationId(Id):
    pass


class NotificationTitle(LongString):
    pass


class NotificationMessage(StringVo):
    max_length = NOTIFICATION_MESSAGE_MAX_LENGTH


class NotificationCreatePayload(AbstractCreatePayload):
    user_id: Id
    title: NotificationTitle
    message: NotificationMessage


class NotificationUpdatePayload(AbstractUpdatePayload):
    id_: NotificationId
    is_read: bool | None = None
