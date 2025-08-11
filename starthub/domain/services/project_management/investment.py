from domain.constants import PROJECT_INVESTMENTS_ORGANIZATIONS_MAX_AMOUNT
from domain.enums.permission import ActionEnum, ScopeEnum
from domain.exceptions.permissions import AddDeniedPermissionException, UpdateDeniedPermissionException
from domain.exceptions.project_management import ProjectInvestmentMaxAmountException
from domain.models.project_management.investment import ProjectInvestment, ProjectInvestmentSocialLink
from domain.models.project_management.project import Project
from domain.models.user import User
from domain.ports.service import AbstractDomainService
from domain.repositories.project.investment import (
    ProjectInestmentReadRepository,
    ProjectInvestmentSocialLinkWriteRepository,
    ProjectInvestmentWriteRepository,
)
from domain.services.permission import PermissionService
from domain.value_objects.common import Id
from domain.value_objects.filter import ProjectInvestmentFilter
from domain.value_objects.project.investment import ProjectInvestmentCreatePayload, ProjectInvestmentUpdatePayload
from domain.value_objects.project.project_investment_social_link import ProjectInvestmentSocialLinkCreatePayload
from loguru import logger


class ProjectInvestmentService(AbstractDomainService):
    def __init__(
        self,
        write_repository: ProjectInvestmentWriteRepository,
        permission_service: PermissionService,
        project_investment_read_repository: ProjectInestmentReadRepository,
    ):
        self._write_repository = write_repository
        self._permission_service = permission_service
        self._project_investment_read_repository = project_investment_read_repository

    def create(self, user: User, project: Project, payload: ProjectInvestmentCreatePayload) -> ProjectInvestment:
        """
        :raises ProjectInvestmentMaxAmountException:
        :raises AddDeniedPermissionException:
        """
        self._check_investment_organizations_amount(project=project)
        self._check_create_permissions(user=user, project=project)

        return self._write_repository.create(data=payload)

    def _check_investment_organizations_amount(self, project: Project) -> None:
        """:raises ProjectInvestmentMaxAmountException:"""

        investments: list[ProjectInvestment] = self._project_investment_read_repository.get_all(
            filter_=ProjectInvestmentFilter(project_id=Id(value=project.id))
        )
        if not (len(investments) < PROJECT_INVESTMENTS_ORGANIZATIONS_MAX_AMOUNT):
            raise ProjectInvestmentMaxAmountException(
                f"Project already has max allowed organizations amount. Max allowed: {PROJECT_INVESTMENTS_ORGANIZATIONS_MAX_AMOUNT}"
            )

        return None

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
            f"User(id={user.id}) doesn't have enough permission to add ProjectInvestment to the Project(id={project.id})."
        )
        raise AddDeniedPermissionException("You don't have enough permission to add this resource.")

    def update(self, user: User, project: Project, payload: ProjectInvestmentUpdatePayload) -> None:
        self._check_udpate_permissions(user=user, project=project)
        self._write_repository.update(data=payload)

    def _check_udpate_permissions(self, user: User, project: Project) -> None:
        """:raises UpdateDeniedPermissionException:"""

        add_own_permission = self._permission_service.create_permission_vo(
            model=ProjectInvestment,
            action=ActionEnum.CHANGE,
            scope=ScopeEnum.OWN,
        )
        has_permission = self._permission_service.has_user_permission(user=user, permission_vo=add_own_permission)
        if has_permission:
            if project.creator == user:
                return None

        logger.exception(
            f"User(id={user.id}) doesn't have enough permission to change ProjectInvestment to the Project(id={project.id})."
        )
        raise UpdateDeniedPermissionException("You don't have enough permission to change this resource.")


# ======================================================================================================================


class ProjectInvestmentSocialLinkService(AbstractDomainService):
    def __init__(
        self,
        write_repository: ProjectInvestmentSocialLinkWriteRepository,
    ):
        self._write_repository = write_repository

    def create(self, payload: ProjectInvestmentSocialLinkCreatePayload) -> ProjectInvestmentSocialLink:
        return self._write_repository.create(data=payload)
