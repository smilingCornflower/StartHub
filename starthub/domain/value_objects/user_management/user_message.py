from domain.ports.command import BaseCommand
from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects.common import Id


class UserMessageId(Id):
    pass


class UserMessageCreatePayload(AbstractCreatePayload):
    pass


class UserMessageUpdatePayload(AbstractUpdatePayload):
    pass


class UserMessageCreateCommand(BaseCommand):
    pass
