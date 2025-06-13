from domain.value_objects.common import Id
from domain.value_objects.project_management import TeamMemberCreateCommand, TeamMemberCreatePayload


def convert_team_members_create_command_to_payload(
    team_members: list[TeamMemberCreateCommand], project_id: Id
) -> list[TeamMemberCreatePayload]:
    return [
        TeamMemberCreatePayload(
            project_id=project_id,
            first_name=member.first_name,
            last_name=member.last_name,
            description=member.description,
        )
        for member in team_members
    ]
