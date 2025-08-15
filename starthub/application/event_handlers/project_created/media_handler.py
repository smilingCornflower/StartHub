from application.services.project_management.project_media import ProjectMediaAppService
from domain.events.project import ProjectCreatedEvent
from domain.ports.event import AbstractEventHandler
from domain.value_objects.project.media import ProjectMediaCreateCommand
from loguru import logger


class ProjectCreatedProjectMediaHandler(AbstractEventHandler[ProjectCreatedEvent]):
    def __init__(self, project_media_app_service: ProjectMediaAppService):
        self._project_media_app_service = project_media_app_service

    def handle(self, event: ProjectCreatedEvent) -> None:
        command = event.command
        user_id = event.user_id
        project_id = event.project_id

        for m in command.media:
            self._project_media_app_service.create(
                user_id=user_id, project_id=project_id, command=ProjectMediaCreateCommand(media=m)
            )
        logger.info("All media created successfully.")
