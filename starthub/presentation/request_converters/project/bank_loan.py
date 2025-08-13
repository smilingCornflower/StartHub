from domain.value_objects.project.bank_loan import LoanAmount, LoanTerms, OrganizationName, ProjectBankLoanCreateCommand
from presentation.request_converters.common import get_required_field
from rest_framework.request import Request


def request_to_bank_loan_create_command(request: Request) -> ProjectBankLoanCreateCommand:
    data = request.data
    return ProjectBankLoanCreateCommand(
        organization_name=OrganizationName(value=get_required_field(data, "organization_name")),
        amount=LoanAmount(value=get_required_field(data, "amount")),
        terms=LoanTerms(value=get_required_field(data, "terms")),
    )
