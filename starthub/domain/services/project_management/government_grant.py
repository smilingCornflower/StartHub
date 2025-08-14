from domain.enums.permission import ActionEnum, ScopeEnum
from domain.exceptions.permissions import (
    AddDeniedPermissionException,
    DeleteDeniedPermissionException,
    UpdateDeniedPermissionException,
)
from domain.models.project_management.government_grant import ProjectGovernmentGrant
from domain.models.project_management.project import Project
from domain.models.user import User
from domain.ports.service import AbstractDomainService
from domain.repositories.project.government_grant import ProjectGovernmentGrantWriteRepository
from domain.services.permission import PermissionService
from domain.value_objects.project.government_grant import (
    ProjectGovernmentGrantUpdatePayload,
    ProjectGoverntmentGrantCreatePayload,
)
from loguru import logger


class ProjectGovernmentGrantService(AbstractDomainService):
    def __init__(self, write_repository: ProjectGovernmentGrantWriteRepository, permission_service: PermissionService):
        self._write_repository = write_repository
        self._permission_service = permission_service

    def create(
        self, user: User, project: Project, payload: ProjectGoverntmentGrantCreatePayload
    ) -> ProjectGovernmentGrant:
        self._check_create_permission(user=user, project=project)
        return self._write_repository.create(data=payload)

    def update(
        self, user: User, government_grant: ProjectGovernmentGrant, payload: ProjectGovernmentGrantUpdatePayload
    ) -> None:
        self._check_update_permission(user=user, government_grant=government_grant)
        self._write_repository.update(data=payload)

    def delete(self, user: User, government_grant: ProjectGovernmentGrant) -> None:
        self._check_delete_permission(user=user, government_grant=government_grant)
        self._write_repository.delete(government_grant=government_grant)

    def _check_delete_permission(self, user: User, government_grant: ProjectGovernmentGrant) -> None:
        """:raises DeniedPermissionException:"""
        permission = self._permission_service.create_permission_vo(
            model=ProjectGovernmentGrant, action=ActionEnum.DELETE, scope=ScopeEnum.OWN
        )
        has_permission = self._permission_service.has_user_permission(user=user, permission_vo=permission)
        if has_permission and government_grant.project.creator == user:
            return None
        logger.exception(
            f"User(id={user.id}) doesn't have enough permission to delete government grant with id = {government_grant.id}."
        )
        raise DeleteDeniedPermissionException("You don't have enough permission to delete this resource.")

    def _check_create_permission(self, user: User, project: Project) -> None:
        """:raisess AddDeniedPermissionException:"""

        permission = self._permission_service.create_permission_vo(
            model=ProjectGovernmentGrant, action=ActionEnum.ADD, scope=ScopeEnum.OWN
        )
        has_permission = self._permission_service.has_user_permission(user=user, permission_vo=permission)
        if has_permission and project.creator == user:
            return None
        logger.exception(
            f"User(id={user.id}) doesn't have enough permission to add government grant to Project(id={project.id})"
        )
        raise AddDeniedPermissionException("You don't have enough permission to add this resource.")

    def _check_update_permission(self, user: User, government_grant: ProjectGovernmentGrant) -> None:
        """:raises UpdateDeniedPermissionException:"""
        permission = self._permission_service.create_permission_vo(
            model=ProjectGovernmentGrant, action=ActionEnum.CHANGE, scope=ScopeEnum.OWN
        )
        has_permission = self._permission_service.has_user_permission(user=user, permission_vo=permission)
        if has_permission and government_grant.project.creator == user:
            return None
        logger.exception(
            f"User(id={user.id}) doesn't have enough permission to update government grant with id = {government_grant.id}."
        )
        raise UpdateDeniedPermissionException("You don't have enough permission to change this resource.")
