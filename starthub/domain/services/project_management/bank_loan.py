from domain.enums.permission import ActionEnum, ScopeEnum
from domain.exceptions.permissions import (
    AddDeniedPermissionException,
    DeleteDeniedPermissionException,
    UpdateDeniedPermissionException,
)
from domain.models.project_management.bank_loan import ProjectBankLoan
from domain.models.project_management.project import Project
from domain.models.user import User
from domain.ports.service import AbstractDomainService
from domain.repositories.project.bank_loan import ProjectBankLoanWriteRepository
from domain.services.permission import PermissionService
from domain.value_objects.project.bank_loan import ProjectBankLoanCreatePaylod, ProjectBankLoanUpdatePayload
from loguru import logger


class ProjectBankLoanPermissionService(AbstractDomainService):
    def __init__(self, permission_service: PermissionService):
        self._permission_service = permission_service

    def _check_create_permission(self, user: User, project: Project) -> None:
        """:raises AddDeniedPermissionException:"""

        create_permission = self._permission_service.create_permission_vo(
            model=ProjectBankLoan,
            action=ActionEnum.ADD,
            scope=ScopeEnum.OWN,
        )
        has_permission = self._permission_service.has_user_permission(user=user, permission_vo=create_permission)

        if has_permission and project.creator == user:
            return None
        logger.exception(f"User(id={user.id}) doesn't have enough permissions to create {ProjectBankLoan.__name__}.")
        raise AddDeniedPermissionException("You don't have enough permissions to create bank loan.")

    def _check_udpate_permission(self, user: User, bank_loan: ProjectBankLoan) -> None:
        """:raises UpdateDeniedPermissionException:"""
        update_permission = self._permission_service.create_permission_vo(
            model=ProjectBankLoan,
            action=ActionEnum.CHANGE,
            scope=ScopeEnum.OWN,
        )
        has_permission = self._permission_service.has_user_permission(user=user, permission_vo=update_permission)

        if has_permission and bank_loan.project.creator == user:
            return None

        logger.exception(f"User(id={user.id}) doesn't have enough permissions to update {ProjectBankLoan.__name__}.")
        raise UpdateDeniedPermissionException("You don't have enough permissions to update bank loan.")

    def _check_delete_permission(self, user: User, bank_loan: ProjectBankLoan) -> None:
        """:raises DeleteDeniedPermissionException:"""
        delete_permission = self._permission_service.create_permission_vo(
            model=ProjectBankLoan,
            action=ActionEnum.DELETE,
            scope=ScopeEnum.OWN,
        )
        has_permission = self._permission_service.has_user_permission(user=user, permission_vo=delete_permission)

        if has_permission and bank_loan.project.creator == user:
            return None

        logger.exception(f"User(id={user.id}) doesn't have enough permissions to delete {ProjectBankLoan.__name__}.")
        raise DeleteDeniedPermissionException("You don't have enough permissions to delete bank loan.")


class ProjectBankLoanService(ProjectBankLoanPermissionService):
    def __init__(
        self,
        write_repository: ProjectBankLoanWriteRepository,
        permission_service: PermissionService,
    ):
        super().__init__(permission_service=permission_service)
        self._write_repository = write_repository

    def create(self, user: User, project: Project, payload: ProjectBankLoanCreatePaylod) -> None:
        self._check_create_permission(user=user, project=project)
        self._write_repository.create(data=payload)

    def update(self, user: User, bank_loan: ProjectBankLoan, payload: ProjectBankLoanUpdatePayload) -> None:
        self._check_udpate_permission(user=user, bank_loan=bank_loan)
        self._write_repository.update(data=payload)

    def delete(self, user: User, bank_loan: ProjectBankLoan) -> None:
        self._check_delete_permission(user=user, bank_loan=bank_loan)
        self._write_repository.delete(bank_loan=bank_loan)
