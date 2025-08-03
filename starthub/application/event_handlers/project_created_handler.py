from domain.events.project import ProjectCreatedEvent
from domain.models import ProjectPhone
from domain.models.company import Company, CompanyFounder
from domain.models.project import ProjectImage
from domain.ports.event import AbstractEventHandler
from domain.services.company import CompanyFounderService, CompanyService
from domain.services.project_management.project_image import ProjectImageService
from domain.services.project_management.project_phone import ProjectPhoneService
from domain.services.project_management.project_social_link import ProjectSocialLinkService
from domain.services.project_management.team_member import TamMemberService
from domain.value_objects.common import Id
from domain.value_objects.company import CompanyCreateCommand, CompanyFounderCreateCommand, CompanyFounderCreatePayload
from domain.value_objects.project_management import (
    ProjectCreateCommand,
    ProjectImageCreateCommand,
    ProjectPhoneCreatePayload,
    ProjectSocialLinkCreatePayload,
)
from loguru import logger


class ProjectCreatedEventHandler(AbstractEventHandler[ProjectCreatedEvent]):
    def __init__(
        self,
        company_service: CompanyService,
        company_founder_service: CompanyFounderService,
        project_image_service: ProjectImageService,
        team_member_service: TamMemberService,
        project_phone_service: ProjectPhoneService,
        social_link_service: ProjectSocialLinkService,
    ):
        self._company_service = company_service
        self._company_founder_service = company_founder_service
        self._project_image_service = project_image_service
        self._team_member_service = team_member_service
        self._project_phone_service = project_phone_service
        self._social_link_service = social_link_service

    def handle(self, event: ProjectCreatedEvent) -> None:
        logger.info(f"Event: {event.event_type} caught.")

        command = event.command
        project_id: Id = event.project_id

        self._create_company_and_founder(command=command, project_id=project_id)
        self._create_images(command=command, project_id=project_id)
        self._create_project_phone(command=command, project_id=project_id)
        self._create_social_links(command=command, project_id=project_id)

    def _create_company_and_founder(self, command: ProjectCreateCommand, project_id: Id) -> None:
        company = self._create_company(command=command, project_id=project_id)
        logger.debug("Company created.")
        self._create_company_founder(command=command, company_id=Id(value=company.id))
        logger.debug("Company founder created.")

    def _create_company(self, command: ProjectCreateCommand, project_id: Id) -> Company:
        company_create_command = CompanyCreateCommand(
            project_id=project_id,
            name=command.company_name,
            country_code=command.country_code,
            business_id=command.business_id,
            established_date=command.established_date,
            description=command.description,
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

    def _create_images(self, command: ProjectCreateCommand, project_id: Id) -> None:
        for image in command.images:
            project_image: ProjectImage = self._project_image_service.create(
                command=ProjectImageCreateCommand(user_id=command.creator_id, project_id=project_id, image_file=image)
            )
            logger.debug(f"ProjectImage uploaded successufully to the path: {project_image.file_path}")
        logger.info("All images uploaded successfully.")

    def _create_project_phone(self, command: ProjectCreateCommand, project_id: Id) -> None:
        project_phone: ProjectPhone = self._project_phone_service.create(
            ProjectPhoneCreatePayload(project_id=project_id, number=command.phone_number)
        )
        logger.debug(f"project_phone with id = {project_phone.id} created successfully.")

    def _create_social_links(self, command: ProjectCreateCommand, project_id: Id) -> None:
        for social_link in command.social_links:
            logger.debug(f"Creating social_link: {social_link}.")
            self._social_link_service.create(
                ProjectSocialLinkCreatePayload(project_id=project_id, social_link=social_link)
            )

        logger.info("All social links created successfully.")
