from domain.value_objects.common import Id
from domain.value_objects.company import CompanyFounderCreateCommand, CompanyFounderCreatePayload


def convert_company_founder_command_to_payload(
    command: CompanyFounderCreateCommand, company_id: Id
) -> CompanyFounderCreatePayload:
    return CompanyFounderCreatePayload(
        company_id=company_id,
        name=command.name,
        surname=command.surname,
        description=command.description,
    )
