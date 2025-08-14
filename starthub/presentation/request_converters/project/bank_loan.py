from domain.value_objects.project.bank_loan import (
    BankLoanOrganizationName,
    LoanAmount,
    LoanTerms,
    ProjectBankLoanCreateCommand,
    ProjectBankLoanUpdateCommand,
)
from presentation.request_converters.common import get_required_field
from rest_framework.request import Request


def request_to_bank_loan_create_command(request: Request) -> ProjectBankLoanCreateCommand:
    data = request.data
    return ProjectBankLoanCreateCommand(
        organization_name=BankLoanOrganizationName(value=get_required_field(data, "organization_name")),
        amount=LoanAmount(value=get_required_field(data, "amount")),
        terms=LoanTerms(value=get_required_field(data, "terms")),
    )


def request_to_bank_loan_update_command(request: Request) -> ProjectBankLoanUpdateCommand:
    data = request.data
    return ProjectBankLoanUpdateCommand(
        organization_name=(
            BankLoanOrganizationName(value=data["organization_name"]) if "organization_name" in data else None
        ),
        amount=LoanAmount(value=data["amount"]) if "amount" in data else None,
        terms=LoanTerms(value=data["terms"]) if "terms" in data else None,
    )
