from abc import ABC, abstractmethod

from domain.models import ProjectBankLoan
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import CursorPagination, OffsetPagination
from domain.value_objects.filter import ProjectBankLoanFilter
from domain.value_objects.project.bank_loan import (
    ProjectBankLoanCreatePaylod,
    ProjectBankLoanId,
    ProjectBankLoanUpdatePayload,
)


class ProjectBankLoanReadRepository(
    AbstractReadRepository[ProjectBankLoan, ProjectBankLoanFilter, ProjectBankLoanId], ABC
):
    @abstractmethod
    def get_by_id(self, id_: ProjectBankLoanId) -> ProjectBankLoan:
        pass

    @abstractmethod
    def get_all(
        self, filter_: ProjectBankLoanFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[ProjectBankLoan]:
        pass


class ProjectBankLoanWriteRepository(
    AbstractWriteRepository[
        ProjectBankLoan, ProjectBankLoanCreatePaylod, ProjectBankLoanUpdatePayload, ProjectBankLoanId
    ],
    ABC,
):
    @abstractmethod
    def create(self, data: ProjectBankLoanCreatePaylod) -> ProjectBankLoan:
        pass

    @abstractmethod
    def update(self, data: ProjectBankLoanUpdatePayload) -> ProjectBankLoan:
        pass

    @abstractmethod
    def delete_by_id(self, id_: ProjectBankLoanId) -> None:
        pass

    @abstractmethod
    def delete(self, bank_loan: ProjectBankLoan) -> None:
        pass
