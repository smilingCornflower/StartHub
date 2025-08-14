from domain.exceptions.project_management import ProjectBankLoanNotFoundException
from domain.models.project_management.bank_loan import ProjectBankLoan
from domain.repositories.project.bank_loan import ProjectBankLoanReadRepository, ProjectBankLoanWriteRepository
from domain.value_objects.common import Pagination
from domain.value_objects.filter import ProjectBankLoanFilter
from domain.value_objects.project.bank_loan import (
    ProjectBankLoanCreatePaylod,
    ProjectBankLoanId,
    ProjectBankLoanUpdatePayload,
)
from infrastructure.repositories.pagination import apply_pagination


class DjProjectBankLoanReadRepository(ProjectBankLoanReadRepository):
    def get_by_id(self, id_: ProjectBankLoanId) -> ProjectBankLoan:
        """:raises ProjectBankLoanNotFoundException:"""
        bank_loan: ProjectBankLoan | None = ProjectBankLoan.objects.filter(id=id_.value).first()
        if bank_loan is None:
            raise ProjectBankLoanNotFoundException(f"ProjectBankLoad with id = {id_.value} not found.")
        return bank_loan

    def get_all(self, filter_: ProjectBankLoanFilter, pagination: Pagination | None = None) -> list[ProjectBankLoan]:
        queryset = ProjectBankLoan.objects.all()

        if filter_.project_id:
            queryset = queryset.filter(project_id=filter_.project_id.value)

        if pagination:
            return apply_pagination(queryset=queryset, pagination=pagination)

        return list(queryset)


class DjProjectBankLoanWriteRepository(ProjectBankLoanWriteRepository):
    def create(self, data: ProjectBankLoanCreatePaylod) -> ProjectBankLoan:
        return ProjectBankLoan.objects.create(
            project_id=data.project_id.value,
            organization_name=data.organization_name.value,
            amount=data.amount.value,
            terms=data.terms.value,
        )

    def update(self, data: ProjectBankLoanUpdatePayload) -> ProjectBankLoan:
        bank_loan: ProjectBankLoan | None = ProjectBankLoan.objects.filter(id=data.loan_id.value).first()

        if bank_loan is None:
            raise ProjectBankLoanNotFoundException(f"ProjectBankLoad with id = {data.loan_id.value} not found.")

        if data.organization_name is not None:
            bank_loan.organization_name = data.organization_name.value
        if data.amount is not None:
            bank_loan.amount = data.amount.value
        if data.terms is not None:
            bank_loan.terms = data.terms.value

        bank_loan.save()
        return bank_loan

    def delete_by_id(self, id_: ProjectBankLoanId) -> None:
        raise NotImplementedError("The method delete_by_id() is not implemented yet.")

    def delete(self, bank_loan: ProjectBankLoan) -> None:
        bank_loan.delete()
