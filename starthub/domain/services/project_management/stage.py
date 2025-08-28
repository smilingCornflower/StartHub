from domain.enums.permission import ActionEnum, ScopeEnum
from domain.exceptions.permissions import UpdateDeniedPermissionException
from domain.models.project_management.project_stage import ProjectStage
from domain.models.user_management.user import User
from domain.ports.service import AbstractDomainService
from domain.repositories.project.stage import ProjectStageWriteRepository
from domain.services.permission import PermissionService
from domain.value_objects.project.stage import ProjectStageUpdatePayload
from loguru import logger


class ProjectStagePermissionService(AbstractDomainService):
    def __init__(self, permission_service: PermissionService):
        self._permission_service = permission_service

    def _check_change_any_project_stage(self, user: User) -> None:
        """:raises UpdateDeniedPermissionException:"""
        if self._permission_service.is_allowed_for_user(
            user=user,
            model=ProjectStage,
            action=ActionEnum.CHANGE,
            scope=ScopeEnum.ANY,
        ):
            return None
        raise UpdateDeniedPermissionException("You don't have enough permissions to change project stage.")


class ProjectStageService(ProjectStagePermissionService):
    def __init__(
        self,
        permission_service: PermissionService,
        write_repository: ProjectStageWriteRepository,
    ):
        super().__init__(permission_service=permission_service)
        self._write_repository = write_repository

    def update(self, user: User, payload: ProjectStageUpdatePayload) -> None:
        self._check_change_any_project_stage(user=user)
        self._write_repository.update(data=payload)
        logger.info("ProjectStage updated successfully.")
