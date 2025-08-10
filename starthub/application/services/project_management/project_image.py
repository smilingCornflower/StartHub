from application.ports.service import AbstractAppService
from domain.services.project_management.project_image import ProjectImageService
from domain.value_objects.common import Id
from domain.value_objects.project.image import (
    ProjectImageCreateCommand,
    ProjectImageDeleteCommand,
    ProjectImageUpdateCommand,
)
from loguru import logger


class ProjectImageAppService(AbstractAppService):
    def __init__(self, project_image_service: ProjectImageService):
        self._project_image_service = project_image_service

    def create(self, image_create_command: ProjectImageCreateCommand) -> None:
        self._project_image_service.create(image_create_command)
        logger.info("ProjectImage created successfully.")

    def get_image_urls(self, project_id: Id) -> list[str]:
        """:raises ProjectNotFoundException:"""
        logger.info(f"Get image urls for project with id = {project_id.value}")
        return self._project_image_service.get_urls(project_id=project_id)

    def delete_image(self, command: ProjectImageDeleteCommand) -> None:
        logger.info(f"Deleting image. project_id: {command.project_id.value}, image_order: {command.image_order}")
        self._project_image_service.delete(command=command)
        logger.info(
            f"Image deleted successfully. project_id: {command.project_id.value}, image_order: {command.image_order}"
        )

    def update_project_images(self, command: ProjectImageUpdateCommand) -> None:
        logger.debug(f"{command=}")
        self._project_image_service.update(command)
