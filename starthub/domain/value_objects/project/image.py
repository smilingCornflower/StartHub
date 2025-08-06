from domain.ports.command import BaseCommand
from domain.ports.payload import AbstractCreatePayload, AbstractDeletePayload, AbstractUpdatePayload
from domain.value_objects import BaseVo
from domain.value_objects.common import Id, Order
from domain.value_objects.file import ImageFile


class ProjectImageCreatePayload(AbstractCreatePayload, BaseVo):
    project_id: Id
    file_path: str
    order: int


class ProjectImageUpdatePayload(AbstractUpdatePayload, BaseVo):
    image_id: Id
    order: Order | None = None


class ProjectImageCreateCommand(BaseCommand):
    user_id: Id
    project_id: Id
    image_file: ImageFile


class ProjectImageUpdateCommand(BaseCommand):
    project_id: Id
    user_id: Id
    new_order: list[Order] | None = None


class ProjectImageDeletePayload(AbstractDeletePayload):
    project_id: Id
    image_order: int


class ProjectImageDeleteCommand(BaseCommand):
    project_id: Id
    image_order: int
    user_id: Id
