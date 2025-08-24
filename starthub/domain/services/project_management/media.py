from io import BytesIO

from domain.constants import IMAGE_FILE_FORMATS, PROJECT_MEDIA_MAX_AMOUNT, VIDEO_FILE_FORMATS
from domain.enums.permission import ActionEnum, ScopeEnum
from domain.exceptions import CustomException
from domain.exceptions.permissions import (
    AddDeniedPermissionException,
    DeleteDeniedPermissionException,
    UpdateDeniedPermissionException,
)
from domain.exceptions.project_management import ProjectMediaMaxAmountException
from domain.models.project_management.media import ProjectMedia
from domain.models.project_management.project import Project
from domain.models.user_management.user import User
from domain.ports.cloud_storage import AbstractCloudStorage
from domain.ports.service import AbstractDomainService
from domain.repositories.project.media import ProjectMediaReadRepository, ProjectMediaWriteRepository
from domain.services.file import ImageService, VideoService
from domain.services.permission import PermissionService
from domain.utils.path_provider import PathProvider
from domain.value_objects.cloud_storage import CloudStorageDeletePayload, CloudStorageUploadPayload
from domain.value_objects.common import Id, Order
from domain.value_objects.filter import ProjectMediaFilter
from domain.value_objects.project.media import (
    MediaFile,
    ProjectMediaCreateCommand,
    ProjectMediaCreatePayload,
    ProjectMediaId,
    ProjectMediaUpdateCommand,
    ProjectMediaUpdatePayload,
)
from loguru import logger


class ProjectMediaPermissionService(AbstractDomainService):
    def __init__(self, permission_service: PermissionService):
        self._permission_service = permission_service

    def _check_create_permission(self, user: User, project: Project) -> None:
        """:raises AddDeniedPermissionException:"""
        create_permission = self._permission_service.create_permission_vo(
            model=ProjectMedia,
            action=ActionEnum.ADD,
            scope=ScopeEnum.OWN,
        )
        has_permission = self._permission_service.has_user_permission(user=user, permission_vo=create_permission)
        if has_permission and project.creator == user:
            return None
        logger.exception(
            f"User(id={user.id}) doesn't have enough permissions to add ProjectMedia to Project(id={project.id})"
        )
        raise AddDeniedPermissionException("You don't have enoug permissions to add this recource.")

    def _check_delete_permission(self, user: User, project_media: ProjectMedia) -> None:
        """:raises DeleteDeniedPermissionException:"""
        delete_permission = self._permission_service.create_permission_vo(
            model=ProjectMedia,
            action=ActionEnum.DELETE,
            scope=ScopeEnum.OWN,
        )
        has_permission = self._permission_service.has_user_permission(user=user, permission_vo=delete_permission)
        if has_permission and project_media.project.creator == user:
            return None
        logger.exception(
            f"User(id={user.id}) doesn't have enough permissions to delete ProjectMedia(id={project_media.id})"
        )
        raise DeleteDeniedPermissionException("You don't have enoug permissions to delete this recource.")

    def _check_update_permission(self, user: User, project: Project) -> None:
        """:raises DeleteDeniedPermissionException:"""
        update_permission = self._permission_service.create_permission_vo(
            model=ProjectMedia,
            action=ActionEnum.CHANGE,
            scope=ScopeEnum.OWN,
        )
        has_permission = self._permission_service.has_user_permission(user=user, permission_vo=update_permission)
        if has_permission and project.creator == user:
            return None
        logger.exception(
            f"User(id={user.id}) doesn't have enough permissions to change media for the Project(id={project.id})."
        )
        raise UpdateDeniedPermissionException("You don't have enoug permissions to update this recource.")


class ProjectMediaService(ProjectMediaPermissionService):
    def __init__(
        self,
        write_repository: ProjectMediaWriteRepository,
        read_repository: ProjectMediaReadRepository,
        permission_service: PermissionService,
        clous_storage: AbstractCloudStorage,
    ):
        super().__init__(permission_service=permission_service)
        self._read_repository = read_repository
        self._write_repository = write_repository
        self._cloud_storage = clous_storage

    # CREATE ===========================================================================================================
    def create(self, user: User, project: Project, command: ProjectMediaCreateCommand) -> ProjectMedia:
        project_id = Id(value=project.id)

        self._check_max_amount_of_media(project_id=project_id)
        self._check_create_permission(user=user, project=project)

        file_path = self._upload_media(media=command.media, project_id=project_id)

        media_order = self.get_media_count(project_id=project_id) + 1
        project_media = self._write_repository.create(
            data=ProjectMediaCreatePayload(
                project_id=project_id,
                file_path=file_path,
                order=media_order,
            )
        )
        logger.info("Project media created.")

        return project_media

    def _upload_media(self, media: MediaFile, project_id: Id) -> str:
        if media.file_extension in IMAGE_FILE_FORMATS:
            compressed_media_obj = ImageService.compress_image(file_obj=BytesIO(media.value))
        elif media.file_extension in VIDEO_FILE_FORMATS:
            compressed_media_obj = VideoService.compress_video(file_obj=BytesIO(media.value))
        else:
            logger.critical(f"File extension {media.file_extension} is neither image nor video format")
            raise CustomException(f"Unsupported media type: {media.file_extension}")

        logger.debug("MediaFile compressed successfully")

        file_path: str = PathProvider.get_project_media_path(project_id=project_id, file_extension=media.file_extension)
        self._cloud_storage.upload_file(
            payload=CloudStorageUploadPayload(file_data=compressed_media_obj.read(), file_path=file_path)
        )
        logger.info(f"Media was uploaded by the path: {file_path}")

        return file_path

    def _check_max_amount_of_media(self, project_id: Id) -> None:
        project_media: list[ProjectMedia] = self._read_repository.get_all(
            filter_=ProjectMediaFilter(project_id=project_id)
        )

        if not (len(project_media) < PROJECT_MEDIA_MAX_AMOUNT):
            raise ProjectMediaMaxAmountException(
                f"Maximum amount of media for project {project_id} is {PROJECT_MEDIA_MAX_AMOUNT}"
            )
        return None

    def get_media_count(self, project_id: Id) -> int:
        return len(self._read_repository.get_all(filter_=ProjectMediaFilter(project_id=project_id)))

    # DELETE ===========================================================================================================
    def delete(self, user: User, project_media: ProjectMedia) -> None:
        self._check_delete_permission(user=user, project_media=project_media)

        self._write_repository.delete(project_media=project_media)
        self._reorder_media(project_id=Id(value=project_media.project.id))
        logger.debug("Media record deleted from a database")

        self._cloud_storage.delete_file(payload=CloudStorageDeletePayload(file_path=project_media.file_path))
        logger.debug("Media file deleted from a storage.")

    def _reorder_media(self, project_id: Id) -> None:
        media_lst: list[ProjectMedia] = self._read_repository.get_all(filter_=ProjectMediaFilter(project_id=project_id))
        for i, media in enumerate(media_lst, start=1):
            if i != media.order:
                logger.debug(
                    f"project_media with id: {media.id} does not match with right order."
                    f"\tMedia order: {media.order}, need: {i}."
                    f"\tStarted updating order."
                )
                self._write_repository.update(
                    data=ProjectMediaUpdatePayload(media_id=ProjectMediaId(value=media.id), order=Order(value=i))
                )
                logger.debug("Media order updated successfully.")
            logger.info("Media order reorganized")

    # UPDATE ===========================================================================================================
    def update(self, user: User, project: Project, command: ProjectMediaUpdateCommand) -> None:
        self._check_update_permission(user=user, project=project)
        if command.new_order:
            self._update_order(project=project, new_order=command.new_order)

    def _update_order(self, project: Project, new_order: list[Order]) -> None:
        media_lst: list[ProjectMedia] = self._read_repository.get_all(
            filter_=ProjectMediaFilter(project_id=Id(value=project.id))
        )
        media_lst.sort(key=lambda x: x.order)
        for media, new_ord in zip(media_lst, new_order):
            logger.debug(f"media_id = {media.id}, new_ord = {new_ord}")
            self._write_repository.update(
                data=ProjectMediaUpdatePayload(media_id=ProjectMediaId(value=media.id), order=new_ord)
            )
        logger.info("Order updated successfully.")
