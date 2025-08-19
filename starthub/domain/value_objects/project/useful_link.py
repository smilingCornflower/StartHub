from domain.ports.command import BaseCommand
from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects import BaseVo
from domain.value_objects.common import Id, MediumString


class UsefulLinkId(Id):
    pass


class UsefulLinkName(MediumString):
    pass


class UsefulLink(BaseVo):
    name: UsefulLinkName
    url: str


class UsefulLinkCreatePayload(AbstractCreatePayload):
    project_id: Id
    name: UsefulLinkName
    url: str


class UsefulLinkUpdatePayload(AbstractUpdatePayload):
    pass


class UsefulLinkCreateCommand(BaseCommand):
    name: UsefulLinkName
    url: str


class UsefulLinkUpdateCommand(BaseCommand):
    pass
