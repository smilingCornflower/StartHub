from loguru import logger

from domain.events.project import ProjectCreatedEvent
from domain.ports.event import AbstractEventHandler
from domain.services.project_management.project_social_link import ProjectSocialLinkService
from domain.value_objects.project.social_link import ProjectSocialLinkCreatePayload


class ProjectCreatedSocialLinkHandler(AbstractEventHandler[ProjectCreatedEvent]):
    def __init__(self, project_social_link_service: ProjectSocialLinkService):
        self._project_social_link_service = project_social_link_service

    def handle(self, event: ProjectCreatedEvent) -> None:
        command = event.command
        project_id = event.project_id

        for social_link in command.social_links:
            logger.debug(f"Creating social_link: {social_link}.")
            self._project_social_link_service.create(
                ProjectSocialLinkCreatePayload(project_id=project_id, social_link=social_link)
            )
        logger.info("All social links created successfully.")
