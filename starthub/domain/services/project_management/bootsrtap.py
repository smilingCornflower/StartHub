from domain.enums.permission import ActionEnum, ScopeEnum
from domain.exceptions.permissions import (
    AddDeniedPermissionException,
    DeleteDeniedPermissionException,
    UpdateDeniedPermissionException,
)
from domain.models.project_management.bootstrap import ProjectBootstrap
from domain.models.project_management.project import Project
from domain.models.user import User
from domain.ports.service import AbstractDomainService
from domain.repositories.project.bootstrap import ProjectBootstrapWriteRepository
from domain.services.permission import PermissionService
from domain.value_objects.project.bootstrap import ProjectBootstrapCreatePayload, ProjectBootstrapUpdatePayload
from loguru import logger


class ProjectBootstrapPermissionService(AbstractDomainService):
    def __init__(self, permission_service: PermissionService):
        self._permission_service = permission_service

    def _check_create_permission(self, user: User, project: Project) -> None:
        """:raises AddDeniedPermissionException:"""

        add_permission = self._permission_service.create_permission_vo(
            model=ProjectBootstrap, action=ActionEnum.ADD, scope=ScopeEnum.OWN
        )
        has_permission = self._permission_service.has_user_permission(user=user, permission_vo=add_permission)
        if has_permission and project.creator == user:
            return None
        logger.exception(
            f"User(id={user.id}) doesn't have enough permission to add bootstrap for the Project(id={project.id})"
        )
        raise AddDeniedPermissionException("You don't have enough permission to add this resource.")

    def _check_update_permission(self, user: User, bootstrap: ProjectBootstrap) -> None:
        """:raises UpdateDeniedPermissionException:"""

        update_permission = self._permission_service.create_permission_vo(
            model=ProjectBootstrap, action=ActionEnum.CHANGE, scope=ScopeEnum.OWN
        )
        has_permission = self._permission_service.has_user_permission(user=user, permission_vo=update_permission)
        if has_permission and bootstrap.project.creator == user:
            return None
        logger.exception(
            f"User(id={user.id}) doesn't have enough permission to update {bootstrap.__class__.__name__}(id={bootstrap.id})"
        )
        raise UpdateDeniedPermissionException("You don't have enough permission to update this resource.")

    def _check_delete_permission(self, user: User, bootstrap: ProjectBootstrap) -> None:
        """:raises DeleteDeniedPermissionException:"""

        delete_permission = self._permission_service.create_permission_vo(
            model=ProjectBootstrap, action=ActionEnum.DELETE, scope=ScopeEnum.OWN
        )
        has_permission = self._permission_service.has_user_permission(user=user, permission_vo=delete_permission)
        if has_permission and bootstrap.project.creator == user:
            return None
        logger.exception(
            f"User(id={user.id}) doesn't have enough permission to delete {bootstrap.__class__.__name__}(id={bootstrap.id})"
        )
        raise DeleteDeniedPermissionException("You don't have enough permission to delete this resource.")


class ProjectBootstrapService(ProjectBootstrapPermissionService):
    def __init__(self, write_repository: ProjectBootstrapWriteRepository, permission_service: PermissionService):
        super().__init__(permission_service=permission_service)
        self._write_repository = write_repository

    def create(self, user: User, project: Project, payload: ProjectBootstrapCreatePayload) -> ProjectBootstrap:
        self._check_create_permission(user=user, project=project)
        return self._write_repository.create(data=payload)

    def update(self, user: User, bootstrap: ProjectBootstrap, payload: ProjectBootstrapUpdatePayload) -> None:
        self._check_update_permission(user=user, bootstrap=bootstrap)
        self._write_repository.update(data=payload)

    def delete(self, user: User, bootstrap: ProjectBootstrap) -> None:
        self._check_delete_permission(user=user, bootstrap=bootstrap)
        self._write_repository.delete(bootstrap=bootstrap)
