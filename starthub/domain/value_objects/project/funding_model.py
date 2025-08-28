from domain.ports.command import BaseCommand
from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects.common import Id


class FundingModelId(Id):
    pass


class FundingModelUpdateCommand(BaseCommand):
    name: str | None
    description: str | None
    recommended: bool | None


class FundingModelCreatePayload(AbstractCreatePayload):
    pass


class FundingModelUpdatePayload(AbstractUpdatePayload):
    id_: Id
    name: str | None
    description: str | None
    recommended: bool | None
