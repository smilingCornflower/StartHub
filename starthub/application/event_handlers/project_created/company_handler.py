from loguru import logger

from domain.events.project import ProjectCreatedEvent
from domain.models.company import Company, CompanyFounder
from domain.models.geo.address import Address
from domain.ports.event import AbstractEventHandler
from domain.services.address import AddressService
from domain.services.company import CompanyFounderService, CompanyService
from domain.value_objects.common import Id
from domain.value_objects.company import CompanyCreateCommand, CompanyFounderCreateCommand, CompanyFounderCreatePayload
from domain.value_objects.project.project import ProjectCreateCommand


class ProjectCreatedCompanyHandler(AbstractEventHandler[ProjectCreatedEvent]):
    def __init__(
        self,
        company_service: CompanyService,
        company_founder_service: CompanyFounderService,
        address_service: AddressService,
    ):
        self._company_service = company_service
        self._company_founder_service = company_founder_service
        self._address_service = address_service

    def handle(self, event: ProjectCreatedEvent) -> None:
        command = event.command
        project_id = event.project_id

        company = self._create_company(command=command, project_id=project_id)
        logger.debug("Company created.")
        self._create_company_founder(command=command, company_id=Id(value=company.id))
        logger.debug("Company founder created.")

    def _create_company(self, command: ProjectCreateCommand, project_id: Id) -> Company:
        address: Address = self._address_service.create(command=command.company_address)

        company_create_command = self._convert_project_create_command_to_company_create_command(
            command=command, project_id=project_id, address_id=Id(value=address.id)
        )
        company: Company = self._company_service.create(command=company_create_command)

        logger.debug(f"Company created successfully with id = {company.id}")
        return company

    def _create_company_founder(self, command: ProjectCreateCommand, company_id: Id) -> CompanyFounder:
        founder_create_command: CompanyFounderCreateCommand = command.company_founder
        payload = CompanyFounderCreatePayload(
            company_id=company_id,
            name=founder_create_command.name,
            surname=founder_create_command.surname,
            description=founder_create_command.description,
        )
        founder: CompanyFounder = self._company_founder_service.create(payload=payload)

        logger.debug(f"Founder created with id = {founder.id}")
        return founder

    def _convert_project_create_command_to_company_create_command(
        self,
        command: ProjectCreateCommand,
        project_id: Id,
        address_id: Id,
    ) -> CompanyCreateCommand:
        return CompanyCreateCommand(
            project_id=project_id,
            name=command.company_name,
            country_code=command.country_code,
            business_id=command.business_id,
            established_date=command.established_date,
            description=command.description,
            address_id=address_id,
            patent_number=command.patent_number,
        )
