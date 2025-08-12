from domain.enums.permission import ActionEnum, ScopeEnum
from domain.exceptions.permissions import AddDeniedPermissionException
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


class ProjectGovernmentGrantService(AbstractDomainService):
    def __init__(self, write_repository: ProjectGovernmentGrantWriteRepository, permission_service: PermissionService):
        self._write_repository = write_repository
        self._permission_service = permission_service

    def create(
        self, user: User, project: Project, payload: ProjectGoverntmentGrantCreatePayload
    ) -> ProjectGovernmentGrant:
        self._check_create_permissions(user=user, project=project)
        return self._write_repository.create(data=payload)

    def update(
        self, user: User, government_grant: ProjectGovernmentGrant, payload: ProjectGovernmentGrantUpdatePayload
    ) -> None:
        pass

    def delete(self, user: User, government_grant: ProjectGovernmentGrant) -> None:
        pass

    def _check_create_permissions(self, user: User, project: Project) -> None:
        """:raisess AddDeniedPermissionException:"""

        permission = self._permission_service.create_permission_vo(
            model=ProjectGovernmentGrant, action=ActionEnum.ADD, scope=ScopeEnum.OWN
        )
        has_permission = self._permission_service.has_user_permission(user=user, permission_vo=permission)
        if has_permission and project.creator == user:
            return None
        raise AddDeniedPermissionException("You don't have enough permission to add this resource.")
