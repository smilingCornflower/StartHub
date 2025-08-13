from application.ports.service import AbstractAppService
from domain.constants import PROJECT_BANK_LOAN_MAX_AMOUNT
from domain.exceptions.project_management import ProjectBankLoanMaxAmountException
from domain.models.project_management.bank_loan import ProjectBankLoan
from domain.models.project_management.project import Project
from domain.models.user import User
from domain.repositories.project.bank_loan import ProjectBankLoanReadRepository
from domain.repositories.project.project import ProjectReadRepository
from domain.repositories.user import UserReadRepository
from domain.services.project_management.bank_loan import ProjectBankLoanService
from domain.value_objects.common import Id
from domain.value_objects.filter import ProjectBankLoanFilter
from domain.value_objects.project.bank_loan import (
    ProjectBankLoanCreateCommand,
    ProjectBankLoanCreatePaylod,
    ProjectBankLoanId,
    ProjectBankLoanUpdateCommand,
)
from loguru import logger


class ProjectBankLoanAppService(AbstractAppService):
    def __init__(
        self,
        bank_loan_service: ProjectBankLoanService,
        bank_loan_read_repository: ProjectBankLoanReadRepository,
        user_read_repository: UserReadRepository,
        project_read_repository: ProjectReadRepository,
    ):
        self._bank_load_service = bank_loan_service
        self._bank_loan_read_repository = bank_loan_read_repository
        self._user_read_repository = user_read_repository
        self._project_read_repository = project_read_repository

    def create(self, user_id: Id, project_id: Id, command: ProjectBankLoanCreateCommand) -> None:
        self._check_bank_loan_max_amount(project_id=project_id)

        user: User = self._user_read_repository.get_by_id(id_=user_id)
        project: Project = self._project_read_repository.get_by_id(id_=project_id)
        payload = self._convert_create_command_to_payload(command=command, project_id=project_id)

        self._bank_load_service.create(user=user, project=project, payload=payload)
        logger.info(f"{ProjectBankLoan.__name__} for the Project(id={project_id.value}) created successfully.")

    def update(self, user_id: Id, bank_loan_id: ProjectBankLoanId, command: ProjectBankLoanUpdateCommand) -> None:
        pass

    def delete(self, user_id: Id, bank_loan_id: ProjectBankLoanId) -> None:
        pass

    def _convert_create_command_to_payload(
        self,
        command: ProjectBankLoanCreateCommand,
        project_id: Id,
    ) -> ProjectBankLoanCreatePaylod:
        return ProjectBankLoanCreatePaylod(
            project_id=project_id,
            organization_name=command.organization_name,
            amount=command.amount,
            terms=command.terms,
        )

    def _check_bank_loan_max_amount(self, project_id: Id) -> None:
        """:raises ProjectBankLoanMaxAmountException:"""

        loans: list[ProjectBankLoan] = self._bank_loan_read_repository.get_all(
            filter_=ProjectBankLoanFilter(project_id=project_id)
        )
        if len(loans) < PROJECT_BANK_LOAN_MAX_AMOUNT:
            return None

        raise ProjectBankLoanMaxAmountException(
            f"Project with id = {project_id.value} already has the maximum allowed number of bank loans ({PROJECT_BANK_LOAN_MAX_AMOUNT})."
        )
