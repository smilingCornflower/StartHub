from abc import ABC, abstractmethod

from domain.models.project_management.team_member import TeamMember
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import CursorPagination, Id, OffsetPagination
from domain.value_objects.filter import TeamMemberFilter
from domain.value_objects.project.team_member import TeamMemberCreatePayload, TeamMemberUpdatePayload


class TeamMemberReadRepository(AbstractReadRepository[TeamMember, TeamMemberFilter, Id], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> TeamMember:
        pass

    @abstractmethod
    def get_all(
        self, filter_: TeamMemberFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[TeamMember]:
        pass


class TeamMemberWriteRepository(
    AbstractWriteRepository[TeamMember, TeamMemberCreatePayload, TeamMemberUpdatePayload, Id], ABC
):
    @abstractmethod
    def create(self, data: TeamMemberCreatePayload) -> TeamMember:
        pass

    @abstractmethod
    def update(self, data: TeamMemberUpdatePayload) -> TeamMember:
        pass

    @abstractmethod
    def delete_by_id(self, id_: Id) -> None:
        pass
