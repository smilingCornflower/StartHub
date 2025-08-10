from domain.events.project import ProjectCreatedEvent
from domain.models import ProjectPhone, User
from domain.models.company import Company, CompanyFounder
from domain.models.geo.address import Address
from domain.models.project_management.image import ProjectImage
from domain.models.project_management.project import Project
from domain.models.project_management.step import ProjectStep
from domain.ports.event import AbstractEventHandler
from domain.services.address import AddressService
from domain.services.company import CompanyFounderService, CompanyService
from domain.services.project_management.accelerator import ProjectAcceleratorService
from domain.services.project_management.crowdfunding import ProjectCrowdfundingService
from domain.services.project_management.incubator import IncubatorService
from domain.services.project_management.project_image import ProjectImageService
from domain.services.project_management.project_phone import ProjectPhoneService
from domain.services.project_management.project_social_link import ProjectSocialLinkService
from domain.services.project_management.step import ProjectStepService
from domain.services.project_management.team_member import TamMemberService
from domain.value_objects.common import Id
from domain.value_objects.company import CompanyCreateCommand, CompanyFounderCreateCommand, CompanyFounderCreatePayload
from domain.value_objects.project.accelerator import ProjectAcceleratorCreateCommand, ProjectAcceleratorCreatePayload
from domain.value_objects.project.crowdfunding import ProjectCrowdfundingCreateCommand, ProjectCrowdfundingCreatePayload
from domain.value_objects.project.image import ProjectImageCreateCommand
from domain.value_objects.project.incubator import IncubatorCreateCommand, IncubatorCreatePayload
from domain.value_objects.project.phone import ProjectPhoneCreatePayload
from domain.value_objects.project.project import ProjectCreateCommand
from domain.value_objects.project.social_link import ProjectSocialLinkCreatePayload
from domain.value_objects.project.step import ProjectStepCreatePaylaod
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
        address_service: AddressService,
        project_step_service: ProjectStepService,
        incubator_service: IncubatorService,
        accelerator_service: ProjectAcceleratorService,
        crowdfunding_service: ProjectCrowdfundingService,
    ):
        self._company_service = company_service
        self._company_founder_service = company_founder_service
        self._project_image_service = project_image_service
        self._team_member_service = team_member_service
        self._project_phone_service = project_phone_service
        self._social_link_service = social_link_service
        self._address_service = address_service
        self._project_step_service = project_step_service
        self._incubator_service = incubator_service
        self._accelerator_service = accelerator_service
        self._crowdfunding_service = crowdfunding_service

    def handle(self, event: ProjectCreatedEvent) -> None:
        logger.info(f"Event: {event.event_type} caught.")

        command = event.command
        project_id: Id = Id(value=event.project.id)
        user: User = event.user
        project: Project = event.project

        self._create_company_and_founder(command=command, project_id=project_id)
        self._create_images(command=command, project_id=project_id)
        self._create_project_phone(command=command, project_id=project_id)
        self._create_social_links(command=command, project_id=project_id)
        self._create_project_steps(command=command, project_id=project_id)

        if command.incubator is not None:
            self._create_project_incubator(incubator_command=command.incubator, project_id=project_id)

        if command.accelerator is not None:
            self._create_project_accelerator(accelerator_command=command.accelerator, project_id=project_id)

        if command.crowdunding is not None:
            self._create_project_crowdfunding(user=user, project=project, crowdfunding_command=command.crowdunding)

        logger.info("All related models are created.")

    def _create_project_crowdfunding(
        self, user: User, project: Project, crowdfunding_command: ProjectCrowdfundingCreateCommand
    ) -> None:
        payload = ProjectCrowdfundingCreatePayload(
            project_id=Id(value=project.id),
            name=crowdfunding_command.name,
            amount=crowdfunding_command.amount,
        )
        self._crowdfunding_service.create(user=user, project=project, payload=payload)
        logger.info("Project crowdfunding created successfully.")

    def _create_project_incubator(self, incubator_command: IncubatorCreateCommand, project_id: Id) -> None:
        payload = IncubatorCreatePayload(
            project_id=project_id,
            name=incubator_command.name,
            description=incubator_command.description,
        )
        self._incubator_service.create(payload=payload)
        logger.info("Project incubator created successfully.")

    def _create_project_accelerator(self, accelerator_command: ProjectAcceleratorCreateCommand, project_id: Id) -> None:
        payload = ProjectAcceleratorCreatePayload(
            project_id=project_id,
            name=accelerator_command.name,
            description=accelerator_command.description,
        )
        self._accelerator_service.create(payload=payload)
        logger.info("Accelerator ctreated successfully.")

    def _create_project_steps(self, command: ProjectCreateCommand, project_id: Id) -> None:
        for project_step_create_command in command.steps:
            payload = ProjectStepCreatePaylaod(
                project_id=project_id,
                name=project_step_create_command.name,
                description=project_step_create_command.description,
                date=project_step_create_command.date,
            )
            project_step: ProjectStep = self._project_step_service.create(paylaod=payload)
            logger.debug(f"project_step with id = {project_step.id} created successfully")

    def _create_company_and_founder(self, command: ProjectCreateCommand, project_id: Id) -> None:
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
