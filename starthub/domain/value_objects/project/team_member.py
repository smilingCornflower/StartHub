from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects import BaseVo
from domain.value_objects.common import Description, FirstName, Id, LastName


class TeamMemberCreatePayload(AbstractCreatePayload, BaseVo):
    project_id: Id
    first_name: FirstName
    last_name: LastName
    description: Description


class TeamMemberCreateCommand(BaseVo):
    first_name: FirstName
    last_name: LastName
    description: Description


class TeamMemberUpdatePayload(AbstractUpdatePayload, BaseVo):
    pass
