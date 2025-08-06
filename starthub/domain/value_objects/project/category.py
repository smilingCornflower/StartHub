from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects import BaseVo


class ProjectCategoryCreatePayload(AbstractCreatePayload, BaseVo):
    pass


class ProjectCategoryUpdatePayload(AbstractUpdatePayload, BaseVo):
    pass
