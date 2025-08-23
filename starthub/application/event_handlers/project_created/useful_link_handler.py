from application.services.project_management.useful_link import ProjectUsefulLinkAppService
from domain.events.project import ProjectCreatedEvent
from domain.ports.event import AbstractEventHandler
from loguru import logger


class ProjectCreatedUsefulLinkHandler(AbstractEventHandler[ProjectCreatedEvent]):
    def __init__(self, project_useful_link_app_service: ProjectUsefulLinkAppService):
        self._project_useful_link_app_service = project_useful_link_app_service

    def handle(self, event: ProjectCreatedEvent) -> None:
        command = event.command
        user_id = event.user_id
        project_id = event.project_id

        if command.useful_links:
            for useful_link in command.useful_links:
                logger.debug(f"Creating useful_link: {useful_link}.")
                self._project_useful_link_app_service.create(
                    user_id=user_id, project_id=project_id, command=useful_link
                )
            logger.info("All useful links created successfully.")
        return None
