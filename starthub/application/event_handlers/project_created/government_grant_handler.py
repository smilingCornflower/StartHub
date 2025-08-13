from application.services.project_management.government_grant import GovernmentGrantAppService
from domain.events.project import ProjectCreatedEvent
from domain.ports.event import AbstractEventHandler


class ProjectCreatedGovernmentGrantHandler(AbstractEventHandler[ProjectCreatedEvent]):
    def __init__(self, government_grant_app_service: GovernmentGrantAppService):
        self._government_grant_app_service = government_grant_app_service

    def handle(self, event: ProjectCreatedEvent) -> None:
        command = event.command
        user_id = event.user_id
        project_id = event.project_id

        if command.government_grant is not None:
            self._government_grant_app_service.create(
                user_id=user_id, project_id=project_id, command=command.government_grant
            )
