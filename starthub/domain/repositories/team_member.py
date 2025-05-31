from abc import ABC, abstractmethod

from domain.models.project import TeamMember
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Id
from domain.value_objects.filter import TeamMemberFilter
from domain.value_objects.team_member import TeamMemberCreatePayload, TeamMemberUpdatePayload


class TeamMemberReadRepository(AbstractReadRepository[TeamMember, TeamMemberFilter], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> TeamMember:
        pass

    @abstractmethod
    def get_all(self, filter_: TeamMemberFilter) -> list[TeamMember]:
        pass


class TeamMemberWriteRepository(
    AbstractWriteRepository[TeamMember, TeamMemberCreatePayload, TeamMemberUpdatePayload], ABC
):
    @abstractmethod
    def create(self, data: TeamMemberCreatePayload) -> TeamMember:
        pass

    @abstractmethod
    def update(self, data: TeamMemberUpdatePayload) -> TeamMember:
        pass

    @abstractmethod
    def delete(self, id_: Id) -> None:
        pass
