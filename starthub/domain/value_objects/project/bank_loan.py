from domain.ports.command import BaseCommand
from domain.ports.payload import AbstractCreatePayload
from domain.value_objects import BaseVo
from domain.value_objects.common import Id, LongString, PositiveNumber
from domain.value_objects.geo import AddressUpdatePayload


class ProjectBankLoanId(Id):
    pass


class BankLoanOrganizationName(LongString):
    pass


class LoanAmount(PositiveNumber):
    pass


class LoanTerms(BaseVo):
    value: str


class ProjectBankLoanCreatePaylod(AbstractCreatePayload):
    project_id: Id
    organization_name: BankLoanOrganizationName
    amount: LoanAmount
    terms: LoanTerms


class ProjectBankLoanUpdatePayload(AddressUpdatePayload):
    loan_id: ProjectBankLoanId
    organization_name: BankLoanOrganizationName | None
    amount: LoanAmount | None
    terms: LoanTerms | None


class ProjectBankLoanCreateCommand(BaseCommand):
    organization_name: BankLoanOrganizationName
    amount: LoanAmount
    terms: LoanTerms


class ProjectBankLoanUpdateCommand(BaseCommand):
    organization_name: BankLoanOrganizationName | None
    amount: LoanAmount | None
    terms: LoanTerms | None
