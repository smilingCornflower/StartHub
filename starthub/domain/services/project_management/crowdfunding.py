from domain.enums.permission import ActionEnum, ScopeEnum
from domain.exceptions.permissions import UpdateDeniedPermissionException
from domain.models.project_management.crowdfunding import ProjectCrowdfunding
from domain.models.project_management.project import Project
from domain.models.user import User
from domain.ports.service import AbstractDomainService
from domain.repositories.project.crowdfunding import ProjectCrowdfundingWriteRepository
from domain.services.permission import PermissionService
from domain.value_objects.project.crowdfunding import ProjectCrowdfundingCreatePayload, ProjectCrowdfundingUpdatePayload
from loguru import logger


class ProjectCrowdfundingService(AbstractDomainService):
    def __init__(
        self,
        write_repository: ProjectCrowdfundingWriteRepository,
        permission_service: PermissionService,
    ):
        self._write_repository = write_repository
        self._permission_service = permission_service

    def create(self, payload: ProjectCrowdfundingCreatePayload) -> ProjectCrowdfunding:
        return self._write_repository.create(data=payload)

    def update(self, user: User, payload: ProjectCrowdfundingUpdatePayload) -> None:
        self._write_repository.update(data=payload)

    def _check_update_permissions(self, user: User, crowdfunding: ProjectCrowdfunding) -> None:
        """:raises UpdateDeniedPermissionException:"""

        update_own_permission = self._permission_service.create_permission_vo(
            model=ProjectCrowdfunding, action=ActionEnum.CHANGE, scope=ScopeEnum.OWN
        )
        has_permission = self._permission_service.has_user_permission(user=user, permission_vo=update_own_permission)
        if has_permission:
            project: Project = crowdfunding.project
            if project.creator == user:
                return None
        logger.exception(
            f"User(id={user.id}) doesn't have enough permission to update ProjectCrowdfunding(id={crowdfunding.id})."
        )
        raise UpdateDeniedPermissionException("You don't have enough permission to update this resource.")
