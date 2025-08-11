from domain.enums.permission import ActionEnum, ScopeEnum
from domain.exceptions.permissions import AddDeniedPermissionException
from domain.models.project_management.investment import ProjectInvestment
from domain.models.project_management.project import Project
from domain.models.user import User
from domain.ports.service import AbstractDomainService
from domain.repositories.project.investment import ProjectInvestmentWriteRepository
from domain.services.permission import PermissionService
from domain.value_objects.project.investment import ProjectInvestmentCreatePayload
from loguru import logger


class ProjectInvestmentService(AbstractDomainService):
    def __init__(
        self,
        write_repository: ProjectInvestmentWriteRepository,
        permission_service: PermissionService,
    ):
        self._write_repository = write_repository
        self._permission_service = permission_service

    def create(self, user: User, project: Project, payload: ProjectInvestmentCreatePayload) -> ProjectInvestment:
        self._check_create_permissions(user=user, project=project)
        return self._write_repository.create(data=payload)

    def _check_create_permissions(self, user: User, project: Project) -> None:
        """:raises AddDeniedPermissionException:"""

        add_own_permission = self._permission_service.create_permission_vo(
            model=ProjectInvestment,
            action=ActionEnum.ADD,
            scope=ScopeEnum.OWN,
        )
        has_permission = self._permission_service.has_user_permission(user=user, permission_vo=add_own_permission)
        if has_permission:
            if project.creator == user:
                return None

        logger.exception(
            f"User(id={user.id}) doesn't have enough permission to add ProjectAccelerator to the Project(id={project.id})."
        )
        raise AddDeniedPermissionException("You don't have enough permission to add this resource.")
