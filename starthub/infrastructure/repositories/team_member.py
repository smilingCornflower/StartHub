from domain.exceptions.team_member import TeamMemberNotFoundException
from domain.models.project import TeamMember
from domain.repositories.team_member import TeamMemberReadRepository, TeamMemberWriteRepository
from domain.value_objects.common import Id
from domain.value_objects.filter import TeamMemberFilter
from domain.value_objects.team_member import TeamMemberCreatePayload, TeamMemberUpdatePayload


class DjTeamMemberReadRepository(TeamMemberReadRepository):
    def get_by_id(self, id_: Id) -> TeamMember:
        team_member: TeamMember | None = TeamMember.objects.filter(id=id_.value).first()
        if team_member is None:
            raise TeamMemberNotFoundException(f"Team member with id = {id_.value} does not exist.")
        return team_member

    def get_all(self, filter_: TeamMemberFilter) -> list[TeamMember]:
        return list(TeamMember.objects.all())


class DjTeamMemberWriteRepository(TeamMemberWriteRepository):
    def create(self, data: TeamMemberCreatePayload) -> TeamMember:
        return TeamMember.objects.create(
            project_id=data.project_id.value,
            name=data.first_name.value,
            surname=data.last_name.value,
            description=data.description,
        )

    def update(self, data: TeamMemberUpdatePayload) -> TeamMember:
        raise NotImplementedError("Method update is not implemented yet.")

    def delete(self, id_: Id) -> None:
        raise NotImplementedError("Method delete is not implemented yet.")
