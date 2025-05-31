from domain.models.project import TeamMember
from domain.repositories.team_member import TeamMemberReadRepository, TeamMemberWriteRepository
from domain.value_objects.team_member import TeamMemberCreatePayload


class TamMemberService:
    def __init__(
        self,
        team_member_read_repository: TeamMemberReadRepository,
        team_member_write_repository: TeamMemberWriteRepository,
    ):
        self._team_member_read_repository = team_member_read_repository
        self._team_member_write_repository = team_member_write_repository

    def create(self, payload: TeamMemberCreatePayload) -> TeamMember:
        return self._team_member_write_repository.create(payload)
