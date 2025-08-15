import io

from domain.constants import PROJECT_MEDIA_MAX_AMOUNT
from domain.enums.file_extension import FileExtensionEnum
from domain.enums.permission import ActionEnum, ScopeEnum
from domain.exceptions.file import UnsupportedFileExtensionException
from domain.exceptions.permissions import AddDeniedPermissionException, DeleteDeniedPermissionException
from domain.exceptions.project_management import ProjectMediaMaxAmountException
from domain.models.project_management.media import ProjectMedia
from domain.models.project_management.project import Project
from domain.models.user import User
from domain.ports.cloud_storage import AbstractCloudStorage
from domain.ports.service import AbstractDomainService
from domain.repositories.project.media import ProjectMediaReadRepository, ProjectMediaWriteRepository
from domain.services.permission import PermissionService
from domain.utils.path_provider import PathProvider
from domain.value_objects.cloud_storage import CloudStorageUploadPayload
from domain.value_objects.common import Id
from domain.value_objects.filter import ProjectMediaFilter
from domain.value_objects.project.media import ProjectMediaCreateCommand, ProjectMediaCreatePayload
from filetype import guess
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


class ProjectMediaService(ProjectMediaPermissionService):
    SUPPORTED_FILES = (FileExtensionEnum.PDF, FileExtensionEnum.JPG, FileExtensionEnum.PNG, FileExtensionEnum.MP4)

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

    def create(self, user: User, project: Project, command: ProjectMediaCreateCommand) -> ProjectMedia:
        project_id = Id(value=project.id)

        self._check_max_amount_of_media(project_id=project_id)
        self._check_create_permission(user=user, project=project)
        file_ext = self._validate_file_extesnsion(command.media.value)

        file_path: str = PathProvider.get_project_media_path(project_id=project_id, file_extension=file_ext)

        self._cloud_storage.upload_file(
            payload=CloudStorageUploadPayload(file_data=command.media.value, file_path=file_path)
        )
        logger.info("Media was uploaded")

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

    def _validate_file_extesnsion(self, file_data: bytes) -> str:
        """Validates file type and returns file extension"""
        kind = guess(io.BytesIO(file_data))
        file_ext: str | None = kind.extension if kind else None
        logger.debug(f"{file_ext=}")

        if file_ext not in self.SUPPORTED_FILES:
            logger.exception(f"Unsupported file type: {file_ext}. Expected: {', '.join(self.SUPPORTED_FILES)}")
            raise UnsupportedFileExtensionException(
                f"Unsupported file type: {file_ext}. Expected: {', '.join(self.SUPPORTED_FILES)}"
            )

        return file_ext

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
