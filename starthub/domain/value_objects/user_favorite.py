from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects import BaseVo
from domain.value_objects.common import Id


class UserFavoriteCreatePayload(AbstractCreatePayload, BaseVo):
    user_id: Id
    project_id: Id


class UserFavoriteUpdatePayload(AbstractUpdatePayload, BaseVo):
    pass
