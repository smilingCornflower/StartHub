from domain.events.project import ProjectCreatedEvent
from domain.models.project_management.image import ProjectImage
from domain.ports.event import AbstractEventHandler
from domain.services.project_management.project_image import ProjectImageService
from domain.value_objects.project.image import ProjectImageCreateCommand
from loguru import logger


class ProjectCreatedProjectImageHandler(AbstractEventHandler[ProjectCreatedEvent]):
    def __init__(self, project_image_service: ProjectImageService):
        self._project_image_service = project_image_service

    def handle(self, event: ProjectCreatedEvent) -> None:
        command = event.command
        project_id = event.project_id

        for image in command.images:
            project_image: ProjectImage = self._project_image_service.create(
                command=ProjectImageCreateCommand(user_id=command.creator_id, project_id=project_id, image_file=image)
            )
            logger.debug(f"ProjectImage uploaded successufully to the path: {project_image.file_path}")
        logger.info("All images uploaded successfully.")
