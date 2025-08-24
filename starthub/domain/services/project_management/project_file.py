import io

from domain.enums.file_extension import FileExtensionEnum
from domain.enums.permission import ActionEnum, ScopeEnum
from domain.exceptions.file import UnsupportedFileExtensionException
from domain.exceptions.permissions import AddDeniedPermissionException, DeleteDeniedPermissionException
from domain.models.project_management.project import Project
from domain.models.project_management.project_file import ProjectFile
from domain.models.user_management.user import User
from domain.ports.cloud_storage import AbstractCloudStorage
from domain.ports.service import AbstractDomainService
from domain.repositories.project.project_file import ProjectFileWriteRepository
from domain.services.permission import PermissionService
from domain.utils.path_provider import PathProvider
from domain.value_objects.cloud_storage import CloudStorageDeletePayload, CloudStorageUploadPayload
from domain.value_objects.common import Id
from domain.value_objects.project.project_file import ProjectFileCreateCommand, ProjectFileCreatePayload
from filetype import guess
from loguru import logger


class ProjectFilePermissionService(AbstractDomainService):
    def __init__(self, permission_service: PermissionService):
        self._permission_service = permission_service

    def _check_create_permission(self, user: User, project: Project) -> None:
        """:raises AddDeniedPermissionException:"""
        create_permission = self._permission_service.create_permission_vo(
            model=ProjectFile,
            action=ActionEnum.ADD,
            scope=ScopeEnum.OWN,
        )
        has_permission = self._permission_service.has_user_permission(user=user, permission_vo=create_permission)
        if has_permission and project.creator == user:
            return None
        logger.exception(
            f"User(id={user.id}) doesn't have enough permissions to add ProjectFile to Project(id={project.id})"
        )
        raise AddDeniedPermissionException("You don't have enoug permissions to add this recource.")

    def _check_delete_permission(self, user: User, project_file: ProjectFile) -> None:
        """:raises DeleteDeniedPermissionException:"""
        delete_permission = self._permission_service.create_permission_vo(
            model=ProjectFile,
            action=ActionEnum.DELETE,
            scope=ScopeEnum.OWN,
        )
        has_permission = self._permission_service.has_user_permission(user=user, permission_vo=delete_permission)
        if has_permission and project_file.project.creator == user:
            return None
        logger.exception(
            f"User(id={user.id}) doesn't have enough permissions to delete ProjectFile(id={project_file.id})"
        )
        raise DeleteDeniedPermissionException("You don't have enoug permissions to delete this recource.")


class ProjectFileService(ProjectFilePermissionService):
    SUPPORTED_FILES = (FileExtensionEnum.PDF, FileExtensionEnum.JPG, FileExtensionEnum.PNG, FileExtensionEnum.MP4)

    def __init__(
        self,
        permission_service: PermissionService,
        cloud_storage: AbstractCloudStorage,
        write_repository: ProjectFileWriteRepository,
    ):
        ProjectFilePermissionService.__init__(self, permission_service=permission_service)
        self._write_repository = write_repository
        self._cloud_storage = cloud_storage

    def create(
        self,
        user: User,
        project: Project,
        command: ProjectFileCreateCommand,
    ) -> None:
        self._check_create_permission(user=user, project=project)
        project_id = Id(value=project.id)
        file_ext = self._validate_file_extesnsion(command.file.value)
        file_path: str = PathProvider.get_project_file_path(project_id=project_id, file_extension=file_ext)

        self._cloud_storage.upload_file(
            payload=CloudStorageUploadPayload(file_data=command.file.value, file_path=file_path)
        )
        logger.info("File was uploaded.")

        self._write_repository.create(
            data=ProjectFileCreatePayload(project_id=project_id, file_path=file_path, name=command.name)
        )
        logger.info("Project file was created.")

    def delete(self, user: User, project_file: ProjectFile) -> None:
        file_path = project_file.file_path
        self._check_delete_permission(user=user, project_file=project_file)
        self._write_repository.delete(project_file=project_file)
        self._cloud_storage.delete_file(payload=CloudStorageDeletePayload(file_path=file_path))

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
