from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects.base import BaseVo
from domain.value_objects.common import FirstName, Id, LastName


class TeamMemberCreatePayload(AbstractCreatePayload, BaseVo):
    project_id: Id
    first_name: FirstName
    last_name: LastName
    description: str


class TeamMemberInProjectCreatePayload(BaseVo):
    first_name: FirstName
    last_name: LastName
    description: str


class TeamMemberUpdatePayload(AbstractUpdatePayload, BaseVo):
    pass
