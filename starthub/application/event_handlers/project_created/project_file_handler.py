from application.services.project_management.project_file import ProjectFileAppService
from domain.events.project import ProjectCreatedEvent
from domain.ports.event import AbstractEventHandler
from domain.value_objects.project.project_file import ProjectFileCreateCommand


class ProjectCreatedProjectFileHandler(AbstractEventHandler[ProjectCreatedEvent]):
    def __init__(self, project_file_app_servcie: ProjectFileAppService):
        self._project_file_app_service = project_file_app_servcie

    def handle(self, event: ProjectCreatedEvent) -> None:
        command = event.command
        user_id = event.user_id
        project_id = event.project_id
        if command.files:
            for file in command.files:
                self._project_file_app_service.create(
                    user_id=user_id, project_id=project_id, command=ProjectFileCreateCommand(file=file)
                )
