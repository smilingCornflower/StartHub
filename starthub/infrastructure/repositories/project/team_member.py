from domain.exceptions.project_management import TeamMemberNotFoundException
from domain.models.project_management.team_member import TeamMember
from domain.repositories.project.team_member import TeamMemberReadRepository, TeamMemberWriteRepository
from domain.value_objects.common import CursorPagination, Id, OffsetPagination
from domain.value_objects.filter import TeamMemberFilter
from domain.value_objects.project.team_member import TeamMemberCreatePayload, TeamMemberUpdatePayload


class DjTeamMemberReadRepository(TeamMemberReadRepository):
    def get_by_id(self, id_: Id) -> TeamMember:
        team_member: TeamMember | None = TeamMember.objects.filter(id=id_.value).first()
        if team_member is None:
            raise TeamMemberNotFoundException(f"Team member with id = {id_.value} does not exist.")
        return team_member

    def get_all(
        self, filter_: TeamMemberFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[TeamMember]:
        return list(TeamMember.objects.all())


class DjTeamMemberWriteRepository(TeamMemberWriteRepository):
    def create(self, data: TeamMemberCreatePayload) -> TeamMember:
        return TeamMember.objects.create(
            project_id=data.project_id.value,
            name=data.first_name.value,
            surname=data.last_name.value,
            description=data.description.value,
        )

    def update(self, data: TeamMemberUpdatePayload) -> TeamMember:
        """:raises NotImplementedError:"""
        raise NotImplementedError("Method update is not implemented yet.")

    def delete_by_id(self, id_: Id) -> None:
        """:raises NotImplementedError:"""
        raise NotImplementedError("Method delete is not implemented yet.")
