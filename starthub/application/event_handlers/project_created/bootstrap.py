from application.services.project_management.bootsrtap import ProjectBootstrapAppService
from domain.events.project import ProjectCreatedEvent
from domain.ports.event import AbstractEventHandler


class ProjectCreatedBootstrapHandler(AbstractEventHandler[ProjectCreatedEvent]):
    def __init__(self, bootstrap_app_service: ProjectBootstrapAppService):
        self._bootstrap_app_service = bootstrap_app_service

    def handle(self, event: ProjectCreatedEvent) -> None:
        command = event.command
        user_id = event.user_id
        project_id = event.project_id

        if command.bootstrap is not None:
            self._bootstrap_app_service.create(user_id=user_id, project_id=project_id, command=command.bootstrap)
