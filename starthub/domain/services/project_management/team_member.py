from domain.models.project_management.team_member import TeamMember
from domain.ports.service import AbstractDomainService
from domain.repositories.project_management import TeamMemberReadRepository, TeamMemberWriteRepository
from domain.value_objects.project_management import TeamMemberCreatePayload


class TamMemberService(AbstractDomainService):
    def __init__(
        self,
        team_member_read_repository: TeamMemberReadRepository,
        team_member_write_repository: TeamMemberWriteRepository,
    ):
        self._team_member_read_repository = team_member_read_repository
        self._team_member_write_repository = team_member_write_repository

    def create(self, payload: TeamMemberCreatePayload) -> TeamMember:
        return self._team_member_write_repository.create(payload)
