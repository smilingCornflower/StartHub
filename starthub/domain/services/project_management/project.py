from domain.enums.permission import ActionEnum, ScopeEnum
from domain.exceptions.permissions import DeleteDeniedPermissionException, UpdateDeniedPermissionException
from domain.models.project_management.project import Project
from domain.models.user import User
from domain.ports.service import AbstractDomainService
from domain.repositories.project_management import ProjectWriteRepository
from domain.services.permission import PermissionService
from domain.value_objects.project_management import ProjectCreatePayload, ProjectUpdatePayload
from domain.value_objects.user import PermissionVo
from loguru import logger


class ProjectCreateService(AbstractDomainService):
    def __init__(
        self,
        write_repository: ProjectWriteRepository,
    ):
        self._write_repository = write_repository

    def create(self, payload: ProjectCreatePayload) -> Project:
        project: Project = self._write_repository.create(payload)
        logger.info("Project created successfully.")
        return project


class ProjectUpdateService(AbstractDomainService):
    def __init__(
        self,
        write_repository: ProjectWriteRepository,
        permission_service: PermissionService,
    ):
        self._write_repository = write_repository
        self._permission_service = permission_service

    def update(self, project: Project, user: User, update_payload: ProjectUpdatePayload) -> None:
        self._check_update_permission(user=user, project=project)
        self._write_repository.update(data=update_payload)

    def _check_update_permission(self, user: User, project: Project) -> None:
        if self._has_update_any_permission(user=user):
            return

        change_own_permission: PermissionVo = self._permission_service.create_permission_vo(
            model=Project, action=ActionEnum.CHANGE, scope=ScopeEnum.OWN
        )
        has_permission: bool = self._permission_service.has_user_permission(
            user=user, permission_vo=change_own_permission
        )
        if has_permission:
            if project.creator == user:
                return

        logger.exception(f"User {user} does not have enough permissions to update the project {project}.")
        raise UpdateDeniedPermissionException("You don't have enough permissions to update this project.")

    def _has_update_any_permission(self, user: User) -> bool:
        change_any_permission: PermissionVo = self._permission_service.create_permission_vo(
            model=Project, action=ActionEnum.CHANGE, scope=ScopeEnum.ANY
        )
        has_permission: bool = self._permission_service.has_user_permission(
            user=user, permission_vo=change_any_permission
        )
        return has_permission


class ProjectDeleteService(AbstractDomainService):
    def __init__(
        self,
        write_repository: ProjectWriteRepository,
        permission_service: PermissionService,
    ):
        self._write_repository = write_repository
        self._permission_service = permission_service

    def delete(self, project: Project, user: User) -> None:
        """:raises DeleteDeniedPermissionException:"""

        self._check_delete_permission(project=project, user=user)
        self._write_repository.delete(project=project)

        logger.info("Project deleted successfully.")

    def _check_delete_permission(self, user: User, project: Project) -> None:
        if self._has_delete_any_permission(user=user):
            return

        delete_own_permission: PermissionVo = self._permission_service.create_permission_vo(
            model=Project, action=ActionEnum.DELETE, scope=ScopeEnum.OWN
        )
        has_own_permission: bool = self._permission_service.has_user_permission(
            user=user, permission_vo=delete_own_permission
        )
        if has_own_permission:
            if project.creator == user:
                return

        logger.exception(f"User: {user} does not have enogh permissions to delete the project: {project}")
        raise DeleteDeniedPermissionException("You don't have enough permissions to delete this project.")

    def _has_delete_any_permission(self, user: User) -> bool:
        delete_any_permission: PermissionVo = self._permission_service.create_permission_vo(
            model=Project, action=ActionEnum.DELETE, scope=ScopeEnum.ANY
        )
        has_any_permission: bool = self._permission_service.has_user_permission(
            user=user, permission_vo=delete_any_permission
        )
        return has_any_permission


class ProjectService(ProjectCreateService, ProjectUpdateService, ProjectDeleteService):
    def __init__(self, write_repository: ProjectWriteRepository, permission_service: PermissionService):
        ProjectCreateService.__init__(self, write_repository)
        ProjectUpdateService.__init__(self, write_repository, permission_service)
        ProjectDeleteService.__init__(self, write_repository, permission_service)
