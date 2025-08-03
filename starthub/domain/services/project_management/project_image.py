from domain.constants import PROJECT_IMAGES_MAX_AMOUNT
from domain.exceptions import BusinessRuleException
from domain.exceptions.cloud_storage import FileNotFoundCloudStorageException
from domain.exceptions.permissions import DeleteDeniedPermissionException, UpdateDeniedPermissionException
from domain.exceptions.project_management import ProjectImageMaxAmountException
from domain.models.project import Project, ProjectImage
from domain.ports.cloud_storage import AbstractCloudStorage
from domain.ports.service import AbstractDomainService
from domain.repositories.project_management import (
    ProjectImageReadRepository,
    ProjectImageWriteRepository,
    ProjectReadRepository,
)
from domain.utils.path_provider import PathProvider
from domain.value_objects.cloud_storage import (
    CloudStorageCreateUrlPayload,
    CloudStorageDeletePayload,
    CloudStorageUploadPayload,
)
from domain.value_objects.common import Id, Order
from domain.value_objects.filter import ProjectImageFilter
from domain.value_objects.project_management import (
    ProjectImageCreateCommand,
    ProjectImageCreatePayload,
    ProjectImageDeleteCommand,
    ProjectImageDeletePayload,
    ProjectImageUpdateCommand,
    ProjectImageUpdatePayload,
)
from loguru import logger


class ProjectImageService(AbstractDomainService):
    def __init__(
        self,
        project_image_read_repository: ProjectImageReadRepository,
        project_image_write_repository: ProjectImageWriteRepository,
        project_read_repository: ProjectReadRepository,
        cloud_storage: AbstractCloudStorage,
    ):
        # TODO: move cloud_storage to application layer
        self._project_image_read_repository = project_image_read_repository
        self._project_image_write_repository = project_image_write_repository
        self._project_read_repository = project_read_repository
        self._cloud_storage = cloud_storage

    def create(self, command: ProjectImageCreateCommand) -> ProjectImage:
        """
        :raises ProjectNotFoundException:
        :raises UpdateDeniedPermissionException:
        :raises ProjectImageMaxAmountException:
        :raises BusinessRuleException:
        """

        project: Project = self._project_read_repository.get_by_id(command.project_id)
        if project.creator_id != command.user_id.value:
            logger.debug(f"creator_id = {project.creator_id}; user_id = {command.user_id.value}")
            raise UpdateDeniedPermissionException("You don't have permission to add images to this project")

        image_count = self._get_images_count(project_id=command.project_id)

        if image_count == PROJECT_IMAGES_MAX_AMOUNT:
            logger.exception("Images max amount reached.")
            raise ProjectImageMaxAmountException(f"Project images max limit is {PROJECT_IMAGES_MAX_AMOUNT}")

        if image_count > PROJECT_IMAGES_MAX_AMOUNT:
            logger.critical("Project images amount exceeds allowed max limit!")
            raise BusinessRuleException(f"Project images max limit is {PROJECT_IMAGES_MAX_AMOUNT}")

        img_path: str = PathProvider.get_project_image_path(command.project_id)
        uploaded_path: str = self._cloud_storage.upload_file(
            CloudStorageUploadPayload(file_data=command.image_file.value, file_path=img_path)
        )
        assert img_path == uploaded_path, "Expected and actual paths don't match."

        logger.debug("Project image uploaded.")
        project_image: ProjectImage = self._project_image_write_repository.create(
            ProjectImageCreatePayload(project_id=command.project_id, file_path=img_path, order=image_count + 1)
        )
        logger.debug("project_image created successfully.")

        return project_image

    def _get_images_count(self, project_id: Id) -> int:
        return len(self._project_image_read_repository.get_all(ProjectImageFilter(project_id=project_id)))

    def get_paths(self, project_id: Id) -> list[str]:
        project_images: list[ProjectImage] = self._project_image_read_repository.get_all(
            ProjectImageFilter(project_id=project_id)
        )
        return [i.file_path for i in project_images]

    def get_urls(self, project_id: Id) -> list[str]:
        """:raises ProjectNotFoundException:"""
        self._project_read_repository.get_by_id(project_id)

        project_images: list[ProjectImage] = self._project_image_read_repository.get_all(
            ProjectImageFilter(project_id=project_id)
        )
        project_images.sort(key=lambda x: x.order)
        image_urls: list[str] = list()
        for i in project_images:
            image_url: str = self._cloud_storage.create_url(CloudStorageCreateUrlPayload(file_path=i.file_path))
            image_urls.append(image_url)
        logger.debug(f"Found {len(image_urls)} urls")
        return image_urls

    def delete(self, command: ProjectImageDeleteCommand) -> None:
        """:raises DeleteDeniedPermissionException:"""
        project: Project = self._project_read_repository.get_by_id(command.project_id)

        if project.creator_id != command.user_id.value:
            raise DeleteDeniedPermissionException("You don't have permission to delete image from this project")

        project_image_lst: list[ProjectImage] = self._project_image_read_repository.get_all(
            ProjectImageFilter(project_id=command.project_id, image_order=command.image_order)
        )
        if project_image_lst:
            project_image: ProjectImage = project_image_lst[0]

            self._project_image_write_repository.delete(
                data=ProjectImageDeletePayload(project_id=command.project_id, image_order=command.image_order)
            )
            self.reorder_images(project_id=command.project_id)
            logger.debug("Image record deleted from the database")

            try:
                image_path = project_image.file_path
                logger.debug(f"Deleting file {image_path}")
                self._cloud_storage.delete_file(payload=CloudStorageDeletePayload(file_path=image_path))
                logger.debug("Image file deleted from the cloud storage")
            except FileNotFoundCloudStorageException:
                logger.info("File not found in cloud storage. Ignoring this exception.")

    def reorder_images(self, project_id: Id) -> None:
        images: list[ProjectImage] = self._project_image_read_repository.get_all(
            ProjectImageFilter(project_id=project_id)
        )
        for i, image in enumerate(images, start=1):
            if i != image.order:
                logger.debug(
                    f"project_image with id: {image.id} does not match with right order."
                    f"\tImage order: {image.order}, need: {i}."
                    f"\tStarted updating order."
                )
                self._project_image_write_repository.update(
                    ProjectImageUpdatePayload(image_id=Id(value=image.id), order=Order(value=i))
                )
                logger.debug("Image order updated successfully.")
        logger.info("Images order reorganized")

    def update(self, command: ProjectImageUpdateCommand) -> None:
        """
        :raises ProjectNotFoundException:
        :raises UpdateDeniedPermissionException:
        """
        project: Project = self._project_read_repository.get_by_id(command.project_id)

        if project.creator_id != command.user_id.value:
            raise UpdateDeniedPermissionException("You don't have permission to update images of this project")

        if command.new_order:
            images: list[ProjectImage] = self._project_image_read_repository.get_all(
                ProjectImageFilter(project_id=command.project_id)
            )
            images.sort(key=lambda x: x.order)

            for img, new_ord in zip(images, command.new_order):
                logger.debug(f"img_id = {img.id}, new_ord = {new_ord}")
                self._project_image_write_repository.update(
                    ProjectImageUpdatePayload(image_id=Id(value=img.id), order=new_ord)
                )
            logger.info("Order updated successfully.")
