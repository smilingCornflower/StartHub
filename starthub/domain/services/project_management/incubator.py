from loguru import logger

from domain.enums.permission import ActionEnum, ScopeEnum
from domain.exceptions.permissions import UpdateDeniedPermissionException
from domain.models.project_management.incubator import ProjectIncubator
from domain.models.project_management.project import Project
from domain.models.user import User
from domain.ports.service import AbstractDomainService
from domain.repositories.project.incubator import ProjectIncubatorWriteRepository
from domain.services.permission import PermissionService
from domain.value_objects.project.incubator import IncubatorCreatePayload, IncubatorUpdatePayload


class IncubatorService(AbstractDomainService):
    def __init__(
        self,
        write_repository: ProjectIncubatorWriteRepository,
        permission_service: PermissionService,
    ):
        self._write_repository = write_repository
        self._permission_service = permission_service

    def create(self, payload: IncubatorCreatePayload) -> None:
        self._write_repository.create(data=payload)

    def update(self, user: User, incubator: ProjectIncubator, payload: IncubatorUpdatePayload) -> None:
        self._check_update_permissions(user=user, incubator=incubator)
        self._write_repository.update(data=payload)

    def _check_update_permissions(self, user: User, incubator: ProjectIncubator) -> None:
        """:raises UpdateDeniedPermissionException:"""

        change_own_permission = self._permission_service.create_permission_vo(
            model=ProjectIncubator,
            action=ActionEnum.CHANGE,
            scope=ScopeEnum.OWN,
        )
        has_permission = self._permission_service.has_user_permission(user=user, permission_vo=change_own_permission)
        if has_permission:
            project: Project = incubator.project
            if project.creator == user:
                return None
        logger.exception(
            f"User(id={user.id}) does't have enough permissions to change ProjectIncubator(id={incubator.id})."
        )
        raise UpdateDeniedPermissionException("You don't have enough permissions to change incubator field.")
