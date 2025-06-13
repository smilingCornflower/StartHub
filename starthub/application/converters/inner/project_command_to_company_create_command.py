from domain.value_objects.common import Id
from domain.value_objects.company import CompanyCreateCommand
from domain.value_objects.project_management import ProjectCreateCommand


def convert_project_create_command_to_company_create_command(
    command: ProjectCreateCommand, project_id: Id
) -> CompanyCreateCommand:
    return CompanyCreateCommand(
        project_id=project_id,
        name=command.company_name,
        country_code=command.country_code,
        business_id=command.business_id,
        established_date=command.established_date,
        description=command.description,
    )
