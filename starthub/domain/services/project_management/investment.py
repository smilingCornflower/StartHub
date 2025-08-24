from domain.constants import PROJECT_INVESTMENTS_ORGANIZATIONS_MAX_AMOUNT
from domain.enums.permission import ActionEnum, ScopeEnum
from domain.exceptions.permissions import (
    AddDeniedPermissionException,
    DeleteDeniedPermissionException,
    UpdateDeniedPermissionException,
)
from domain.exceptions.project_management import ProjectInvestmentMaxAmountException
from domain.models.project_management.investment import (
    ProjectInvestment,
    ProjectInvestmentPhone,
    ProjectInvestmentSocialLink,
)
from domain.models.project_management.project import Project
from domain.models.user_management.user import User
from domain.ports.service import AbstractDomainService
from domain.repositories.project.investment import (
    ProjectInvestmentPhoneWriteRepository,
    ProjectInvestmentReadRepository,
    ProjectInvestmentSocialLinkWriteRepository,
    ProjectInvestmentWriteRepository,
)
from domain.services.permission import PermissionService
from domain.value_objects.common import Id
from domain.value_objects.filter import ProjectInvestmentFilter
from domain.value_objects.project.investment import ProjectInvestmentCreatePayload, ProjectInvestmentUpdatePayload
from domain.value_objects.project.project_investment_phone import ProjectInvestmentPhoneCreatePayload
from domain.value_objects.project.project_investment_social_link import ProjectInvestmentSocialLinkCreatePayload
from loguru import logger


class ProjectInvestmentService(AbstractDomainService):
    def __init__(
        self,
        write_repository: ProjectInvestmentWriteRepository,
        permission_service: PermissionService,
        project_investment_read_repository: ProjectInvestmentReadRepository,
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
        permission_service: PermissionService,
    ):
        self._write_repository = write_repository
        self._permission_service = permission_service

    def create(
        self, user: User, project: Project, payload: ProjectInvestmentSocialLinkCreatePayload
    ) -> ProjectInvestmentSocialLink:
        self._check_create_permissions(user=user, project=project)
        return self._write_repository.create(data=payload)

    def delete(
        self,
        user: User,
        project: Project,
        social_link: ProjectInvestmentSocialLink,
    ) -> None:
        self._check_delete_permissions(user=user, project=project)
        self._write_repository.delete(investment=social_link)

    def _check_delete_permissions(self, user: User, project: Project) -> None:
        """:raises DeleteDeniedPermissionException:"""
        add_own_permission = self._permission_service.create_permission_vo(
            model=ProjectInvestment,
            action=ActionEnum.DELETE,
            scope=ScopeEnum.OWN,
        )
        has_permission = self._permission_service.has_user_permission(user=user, permission_vo=add_own_permission)
        if has_permission:
            if project.creator == user:
                return None

        logger.exception(
            f"User(id={user.id}) doesn't have enough permission to delete ProjectInvestmentSocialLink to the Project(id={project.id})."
        )
        raise DeleteDeniedPermissionException("You don't have enough permission to delete this resource.")

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
            f"User(id={user.id}) doesn't have enough permission to add ProjectInvestmentSocialLink to the Project(id={project.id})."
        )
        raise AddDeniedPermissionException("You don't have enough permission to add this resource.")


# ======================================================================================================================


class ProjectInvestmentPhoneService(AbstractDomainService):
    def __init__(self, write_repository: ProjectInvestmentPhoneWriteRepository, permission_service: PermissionService):
        self._write_repository = write_repository
        self._permission_service = permission_service

    def create(self, user: User, project: Project, payload: ProjectInvestmentPhoneCreatePayload) -> None:
        self._check_create_permissions(user=user, project=project)
        self._write_repository.create(data=payload)

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
            f"User(id={user.id}) doesn't have enough permission to add ProjectInvestmentPhone to the Project(id={project.id})."
        )
        raise AddDeniedPermissionException("You don't have enough permission to add this resource.")

    def delete(self, user: User, project: Project, phone_number: ProjectInvestmentPhone) -> None:
        self._check_delete_permissions(user=user, project=project)
        self._write_repository.delete(investment_phone=phone_number)

    def _check_delete_permissions(self, user: User, project: Project) -> None:
        """:raises DeleteDeniedPermissionException:"""
        add_own_permission = self._permission_service.create_permission_vo(
            model=ProjectInvestment,
            action=ActionEnum.DELETE,
            scope=ScopeEnum.OWN,
        )
        has_permission = self._permission_service.has_user_permission(user=user, permission_vo=add_own_permission)
        if has_permission:
            if project.creator == user:
                return None

        logger.exception(
            f"User(id={user.id}) doesn't have enough permission to delete ProjectInvestmentPhone to the Project(id={project.id})."
        )
        raise DeleteDeniedPermissionException("You don't have enough permission to delete this resource.")
