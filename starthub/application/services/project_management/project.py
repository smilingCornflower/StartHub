from dataclasses import asdict

from application.converters.resposne_converters.project import project_to_dto
from application.dto.project import (
    AcceleratorDto,
    CrowdfundingDto,
    IncubatorDto,
    ProjectDto,
    ProjectFullDto,
    ProjectInvestmentDto,
    ProjectStepDto,
    SocialLinkDto,
)
from application.ports.service import AbstractAppService
from django.db import transaction
from domain.enums.project_status import ProjectStatusEnum
from domain.events.project import ProjectCreatedEvent, ProjectDeletedEvent
from domain.exceptions.company import BusinessNumberAlreadyExistsException
from domain.exceptions.geo.country import CountryNotFoundException
from domain.exceptions.project_management import ProjectCategoryNotFoundException, ProjectPlanNotFoundException
from domain.exceptions.user_favorite import UserFavoriteNotFoundException
from domain.models import Country
from domain.models.company import Company
from domain.models.project_management.accelerator import ProjectAccelerator
from domain.models.project_management.category import ProjectCategory
from domain.models.project_management.crowdfunding import ProjectCrowdfunding
from domain.models.project_management.image import ProjectImage
from domain.models.project_management.incubator import ProjectIncubator
from domain.models.project_management.investment import (
    ProjectInvestment,
    ProjectInvestmentPhone,
    ProjectInvestmentSocialLink,
)
from domain.models.project_management.project import Project
from domain.models.project_management.step import ProjectStep
from domain.models.user import User
from domain.ports.cloud_storage import AbstractCloudStorage
from domain.repositories.company import CompanyReadRepository
from domain.repositories.country import CountryReadRepository
from domain.repositories.geo.city import CityReadRepository
from domain.repositories.geo.region import RegionReadRepository
from domain.repositories.project.accelerator import ProjectAcceleratorReadRepository
from domain.repositories.project.category import ProjectCategoryReadRepository
from domain.repositories.project.crowdfunding import ProjectCrowdfundingReadRepository
from domain.repositories.project.funding_model import FundingModelReadRepository
from domain.repositories.project.image import ProjectImageReadRepository
from domain.repositories.project.incubator import PojectIncubatorReadRepository
from domain.repositories.project.investment import (
    ProjectInvestmentPhoneReadRepository,
    ProjectInvestmentReadRepository,
    ProjectInvestmentSocialLinkReadRepository,
)
from domain.repositories.project.project import ProjectReadRepository
from domain.repositories.project.step import ProjectStepReadRepository
from domain.repositories.user import UserReadRepository
from domain.repositories.user_favorite import UserFavoriteReadRepository
from domain.services.project_management.accelerator import ProjectAcceleratorService
from domain.services.project_management.incubator import IncubatorService
from domain.services.project_management.project import ProjectService
from domain.services.project_management.step import ProjectStepService
from domain.utils.path_provider import PathProvider
from domain.value_objects.cloud_storage import CloudStorageCreateUrlPayload, CloudStorageUploadPayload
from domain.value_objects.common import Id, OffsetPagination, Pagination
from domain.value_objects.company import BusinessNumber
from domain.value_objects.country import CountryCode
from domain.value_objects.file import PdfFile
from domain.value_objects.filter import (
    CompanyFilter,
    CountryFilter,
    ProjectAcceleratorFilter,
    ProjectCategoryFilter,
    ProjectCrowdfundingFilter,
    ProjectFilter,
    ProjectImageFilter,
    ProjectIncubatorFilter,
    ProjectInvestmentFilter,
    ProjectInvestmentPhoneFilter,
    ProjectInvestmentSocialLinkFilter,
    ProjectStepFilter,
)
from domain.value_objects.geo import CityId, RegionId
from domain.value_objects.project.common import ProjectStatus
from domain.value_objects.project.incubator import IncubatorCreatePayload, IncubatorUpdatePayload
from domain.value_objects.project.investment import ProjectInvestmentId
from domain.value_objects.project.project import (
    ProjectCreateCommand,
    ProjectCreatePayload,
    ProjectUpdateCommand,
    ProjectUpdatePayload,
)
from domain.value_objects.project.step import ProjectStepCreateCommand, ProjectStepCreatePaylaod
from domain.value_objects.search import ProjectSearchParams
from infrastructure.event_bus import EventBus
from infrastructure.services.project_search import ProjectSearchService
from loguru import logger


class ProjectCreateAppService(AbstractAppService):
    def __init__(
        self,
        project_service: ProjectService,
        project_step_service: ProjectStepService,
        cloud_storage: AbstractCloudStorage,
        user_read_repository: UserReadRepository,
        funding_model_read_repository: FundingModelReadRepository,
        company_read_repository: CompanyReadRepository,
        country_read_repository: CountryReadRepository,
        project_category_read_repository: ProjectCategoryReadRepository,
        city_read_repository: CityReadRepository,
        region_read_repository: RegionReadRepository,
    ):
        self._project_service = project_service
        self._project_step_service = project_step_service
        self._cloud_storage = cloud_storage
        self._user_read_repository = user_read_repository
        self._funding_model_read_repository = funding_model_read_repository
        self._company_read_repository = company_read_repository
        self._country_read_repository = country_read_repository
        self._project_category_read_repository = project_category_read_repository
        self._city_read_repository = city_read_repository
        self._region_read_repository = region_read_repository

    def create(self, command: ProjectCreateCommand, user_id: Id) -> Project:
        logger.warning("Started creating project.")

        self._validate_dependencies(command=command)
        self._project_step_service.check_project_max_steps_limit(project_steps=command.steps)

        plan_path: str = self._upload_plan(plan_file=command.plan_file)
        create_payload: ProjectCreatePayload = self._convert_command_to_payload(command=command, plan_path=plan_path)

        user: User = self._user_read_repository.get_by_id(id_=user_id)
        with transaction.atomic():
            project: Project = self._project_service.create(payload=create_payload)

            event = ProjectCreatedEvent(user=user, project=project, command=command)
            EventBus().publish(event)

        return project

    def _validate_dependencies(self, command: ProjectCreateCommand) -> None:
        self._check_user_exists(user_id=command.creator_id)
        self._check_categories_exist(command.category_ids)
        self._check_funding_model_exists(funding_model_id=command.funding_model_id)
        self._check_business_number_avaiable(business_number=command.business_id)
        self._check_city_exists(city_id=command.company_address.city_id)
        self._check_region_exists(region_id=command.company_address.region_id)

        logger.info("All dependencies validated")

    def _check_region_exists(self, region_id: RegionId) -> None:
        """:raises RegionNotFoundException:"""
        self._region_read_repository.get_by_id(id_=region_id)
        logger.debug(f"Region with id = {region_id.value} exists.")

    def _check_city_exists(self, city_id: CityId) -> None:
        """:raises CityNotFoundException:"""
        self._city_read_repository.get_by_id(id_=city_id)
        logger.debug(f"City with id = {city_id.value} exists.")

    def _check_country_code_exists(self, country_code: CountryCode) -> None:
        """:raises CountryNotFoundException:"""
        countries: list[Country] = self._country_read_repository.get_all(CountryFilter(code=country_code))
        if not countries:
            raise CountryNotFoundException(f"A country with code = {country_code.value} not found.")
        logger.debug("Country code exists.")

    def _check_business_number_avaiable(self, business_number: BusinessNumber) -> None:
        """:raises BusinessNumberAlreadyExistsException:"""
        search_result: list[Company] = self._company_read_repository.get_all(CompanyFilter(business_id=business_number))
        if search_result:
            raise BusinessNumberAlreadyExistsException("This business number already exists.")
        logger.debug("Business number is available.")

    def _check_user_exists(self, user_id: Id) -> None:
        """:raises UserNotFoundException:"""
        self._user_read_repository.get_by_id(id_=user_id)
        logger.debug(f"User with id = {user_id.value} exists.")

    def _check_funding_model_exists(self, funding_model_id: Id) -> None:
        """:raises FundingModelNotFoundException:"""
        self._funding_model_read_repository.get_by_id(id_=funding_model_id)
        logger.debug(f"Funding model with id = {funding_model_id.value} exists.")

    def _check_categories_exist(self, category_ids: list[Id]) -> None:
        """:raises ProjectCategoryNotFoundException:"""
        for category_id in category_ids:
            self._project_category_read_repository.get_by_id(id_=category_id)
            logger.debug(f"Category with id = {category_id.value} exists.")

    def _convert_command_to_payload(self, command: ProjectCreateCommand, plan_path: str) -> ProjectCreatePayload:
        payload = ProjectCreatePayload(
            name=command.name,
            goal_description=command.goal_description,
            description=command.description,
            category_ids=command.category_ids,
            user_id=command.creator_id,
            funding_model_id=command.funding_model_id,
            stage=command.stage,
            status=ProjectStatus(value=ProjectStatusEnum.UNDER_MODERATION),
            goal_sum=command.goal_sum,
            deadline=command.deadline.value,
            plan_path=plan_path,
        )
        return payload

    def _upload_plan(self, plan_file: PdfFile) -> str:
        project_plan_path: str = PathProvider.get_project_plan_path()
        uploaded_path: str = self._cloud_storage.upload_file(
            CloudStorageUploadPayload(file_data=plan_file.value, file_path=project_plan_path)
        )
        logger.debug("Project pdf uploaded.")

        assert project_plan_path == uploaded_path, "File uploaded in unexpected path."
        return uploaded_path


class ProjectGetAppService(AbstractAppService):
    def __init__(
        self,
        project_read_repository: ProjectReadRepository,
        project_image_read_repository: ProjectImageReadRepository,
        project_category_read_repository: ProjectCategoryReadRepository,
        user_favorite_read_repository: UserFavoriteReadRepository,
        project_step_read_repository: ProjectStepReadRepository,
        project_incubator_read_repository: PojectIncubatorReadRepository,
        project_accelerator_read_repository: ProjectAcceleratorReadRepository,
        project_crowdfunding_read_repository: ProjectCrowdfundingReadRepository,
        project_investment_read_repository: ProjectInvestmentReadRepository,
        project_investment_social_link_read_repository: ProjectInvestmentSocialLinkReadRepository,
        project_investment_phone_read_repository: ProjectInvestmentPhoneReadRepository,
        project_search_service: ProjectSearchService,
        cloud_storage: AbstractCloudStorage,
    ):
        self._project_read_repository = project_read_repository
        self._project_image_read_repository = project_image_read_repository
        self._project_category_read_repository = project_category_read_repository
        self._user_favorite_read_repository = user_favorite_read_repository

        self._project_step_read_repository = project_step_read_repository
        self._project_incubator_read_repository = project_incubator_read_repository
        self._project_accelerator_read_repository = project_accelerator_read_repository
        self._project_crowdfunding_read_repository = project_crowdfunding_read_repository
        self._project_investment_read_repository = project_investment_read_repository
        self._project_investment_social_link_read_repository = project_investment_social_link_read_repository
        self._project_investment_phone_read_repository = project_investment_phone_read_repository
        self._project_search_service = project_search_service
        self._cloud_storage = cloud_storage

    def get(self, filter_: ProjectFilter, pagination: Pagination, user_id: Id | None = None) -> list[ProjectDto]:
        projects: list[Project] = self._project_read_repository.get_all(filter_=filter_, pagination=pagination)
        logger.debug(f"Found {len(projects)} projectes.")

        return [self._create_dto(project=project, user_id=user_id) for project in projects]

    def get_by_id(self, project_id: Id, user_id: Id | None = None) -> ProjectDto:
        project: Project = self._project_read_repository.get_by_id(id_=project_id)
        logger.debug(f"Project with id = {project_id.value} found.")

        return self._create_full_dto(project=project, user_id=user_id)

    def get_plan_url(self, project_id: Id) -> str:
        """
        :raises ProjectNotFoundException:
        :raises ProjectPlanNotFoundException:
        """
        project: Project = self._project_read_repository.get_by_id(id_=project_id)
        if project.plan:
            return self._cloud_storage.create_url(CloudStorageCreateUrlPayload(file_path=project.plan))
        raise ProjectPlanNotFoundException(f"No plan found for the project with the id = {project_id.value}")

    def _create_dto(self, project: Project, user_id: Id | None = None) -> ProjectDto:
        project_id: Id = Id(value=project.id)

        categories: list[ProjectCategory] = self._get_categories(project_id=project_id)
        image_urls: list[str] = self._get_image_urls(project_id=project_id)
        is_favorite: bool = self._is_project_favorite(project_id=project_id, user_id=user_id)

        return project_to_dto(project=project, categories=categories, image_links=image_urls, is_favorite=is_favorite)

    def _create_full_dto(self, project: Project, user_id: Id | None = None) -> ProjectFullDto:
        project_id: Id = Id(value=project.id)
        project_dto: ProjectDto = self._create_dto(project=project, user_id=user_id)

        steps: list[ProjectStepDto] = self._get_step_dtos(project_id=project_id)
        incubator: IncubatorDto | None = self._get_incubator_dto_if_present(project_id=project_id)
        accelerator: AcceleratorDto | None = self._get_accelerator_dto_if_present(project_id=project_id)
        crowdfunding: CrowdfundingDto | None = self._get_crowdfunding_dto_if_present(project_id=project_id)
        investments: list[ProjectInvestmentDto] | None = self._get_investment_dto_if_present(project_id=project_id)
        total_investment_amount = sum([i.amount for i in investments]) if investments is not None else 0
        return ProjectFullDto(
            **asdict(project_dto),
            steps=steps,
            incubator=incubator,
            accelerator=accelerator,
            crowdfunding=crowdfunding,
            investments=investments,
            total_investment_amount=total_investment_amount,
        )

    def _get_investment_dto_if_present(self, project_id: Id) -> list[ProjectInvestmentDto] | None:
        result = list()
        investments: list[ProjectInvestment] = self._project_investment_read_repository.get_all(
            filter_=ProjectInvestmentFilter(project_id=project_id)
        )
        logger.debug(f"{investments=}")
        for investment in investments:
            investment_id = ProjectInvestmentId(value=investment.id)
            phones: list[ProjectInvestmentPhone] = self._project_investment_phone_read_repository.get_all(
                filter_=ProjectInvestmentPhoneFilter(investment_id=investment_id)
            )
            social_links: list[ProjectInvestmentSocialLink] = (
                self._project_investment_social_link_read_repository.get_all(
                    filter_=ProjectInvestmentSocialLinkFilter(investment_id=investment_id)
                )
            )
            result.append(
                ProjectInvestmentDto(
                    id=investment.id,
                    organization_name=investment.organization_name,
                    slug=investment.slug,
                    amount=investment.amount,
                    social_links=[SocialLinkDto(platform=i.platform, url=i.url) for i in social_links],
                    phones=[i.number for i in phones],
                )
            )
        return result

    def _get_crowdfunding_dto_if_present(self, project_id: Id) -> CrowdfundingDto | None:
        crowdfundings: list[ProjectCrowdfunding] = self._project_crowdfunding_read_repository.get_all(
            filter_=ProjectCrowdfundingFilter(project_id=project_id)
        )
        if crowdfundings:
            crowdfunding: ProjectCrowdfunding = crowdfundings[0]
            return CrowdfundingDto(id=crowdfunding.id, name=crowdfunding.name, amount=crowdfunding.amount)
        else:
            return None

    def _get_accelerator_dto_if_present(self, project_id: Id) -> AcceleratorDto | None:
        accelerators: list[ProjectAccelerator] = self._project_accelerator_read_repository.get_all(
            filter_=ProjectAcceleratorFilter(project_id=project_id)
        )
        if accelerators:
            accelerator: ProjectAccelerator = accelerators[0]
            return AcceleratorDto(id=accelerator.id, name=accelerator.name, description=accelerator.description)
        else:
            return None

    def _get_incubator_dto_if_present(self, project_id: Id) -> IncubatorDto | None:
        incubators: list[ProjectIncubator] = self._project_incubator_read_repository.get_all(
            filter_=ProjectIncubatorFilter(project_id=project_id)
        )
        if incubators:
            incubator: ProjectIncubator = incubators[0]
            return IncubatorDto(id=incubator.id, name=incubator.name, description=incubator.description)
        else:
            return None

    def _get_step_dtos(self, project_id: Id) -> list[ProjectStepDto]:
        steps: list[ProjectStep] = self._project_step_read_repository.get_all(
            filter_=ProjectStepFilter(project_id=project_id)
        )
        step_dtos: list[ProjectStepDto] = list()
        for i in steps:
            step_dtos.append(ProjectStepDto(id=i.id, name=i.name, description=i.description, date=i.date))
        return step_dtos

    def _is_project_favorite(self, project_id: Id, user_id: Id | None) -> bool:
        if user_id is None:
            return False

        try:
            self._user_favorite_read_repository.get_by_association_ids(user_id=user_id, project_id=project_id)
            return True
        except UserFavoriteNotFoundException:
            logger.debug(f"UserFavorite not found for user_id={user_id}, project_id={project_id}")
            return False

    def _get_categories(self, project_id: Id) -> list[ProjectCategory]:
        return self._project_category_read_repository.get_all(filter_=ProjectCategoryFilter(project_id=project_id))

    def _get_image_urls(self, project_id: Id) -> list[str]:
        image_urls: list[str] = list()
        images: list[ProjectImage] = self._project_image_read_repository.get_all(
            filter_=ProjectImageFilter(project_id=project_id)
        )

        for img in images:
            img_url: str = self._cloud_storage.create_url(payload=CloudStorageCreateUrlPayload(file_path=img.file_path))
            image_urls.append(img_url)

        return image_urls

    def search(
        self, search_params: ProjectSearchParams, offset_pagination: OffsetPagination, user_id: Id | None = None
    ) -> list[ProjectDto]:
        projects: list[Project] = self._project_search_service.search(
            search_params=search_params, pagination=offset_pagination
        )
        result: list[ProjectDto] = [self._create_dto(project=i, user_id=user_id) for i in projects]
        return result


class ProjectDeleteAppService(AbstractAppService):
    def __init__(
        self,
        project_service: ProjectService,
        user_read_repository: UserReadRepository,
        project_read_repository: ProjectReadRepository,
        project_image_read_repository: ProjectImageReadRepository,
    ):
        self._project_service = project_service
        self._user_read_repository = user_read_repository
        self._project_read_repository = project_read_repository
        self._project_image_read_repository = project_image_read_repository

    def delete(self, project_id: Id, user_id: Id) -> None:
        """
        :raises ProjectNotFoundException:
        :raises UserNotFoundException:
        """
        project: Project = self._project_read_repository.get_by_id(id_=project_id)
        user: User = self._user_read_repository.get_by_id(id_=user_id)

        plan_path: str | None = project.plan
        project_image_paths: list[str] = self._get_project_image_paths(project_id=project_id)

        self._project_service.delete(project=project, user=user)
        logger.info("Project model deleted successfully.")
        event = ProjectDeletedEvent(project_id=project_id, plan_file_path=plan_path, image_paths=project_image_paths)
        EventBus().publish(event)

    def _get_project_image_paths(self, project_id: Id) -> list[str]:
        """:raises ProjectNotFoundException:"""
        self._project_read_repository.get_by_id(id_=project_id)  # check

        project_images: list[ProjectImage] = self._project_image_read_repository.get_all(
            filter_=ProjectImageFilter(project_id=project_id)
        )
        return [img.file_path for img in project_images]


class ProjectUpdateAppService(AbstractAppService):
    def __init__(
        self,
        project_service: ProjectService,
        project_step_service: ProjectStepService,
        incubator_service: IncubatorService,
        accelerator_service: ProjectAcceleratorService,
        incubator_read_repository: PojectIncubatorReadRepository,
        accelerator_read_repository: ProjectAcceleratorReadRepository,
        user_read_repository: UserReadRepository,
        project_read_repository: ProjectReadRepository,
        project_category_read_repository: ProjectCategoryReadRepository,
        funding_model_read_repository: FundingModelReadRepository,
        cloud_storage: AbstractCloudStorage,
    ):
        self._project_service = project_service
        self._project_step_service = project_step_service
        self._incubator_service = incubator_service
        self._accelerator_service = accelerator_service
        self._incubator_read_repository = incubator_read_repository
        self._accelerator_read_repository = accelerator_read_repository
        self._user_read_repository = user_read_repository
        self._project_read_repository = project_read_repository
        self._project_category_read_repository = project_category_read_repository
        self._funding_model_read_repository = funding_model_read_repository
        self._cloud_storage = cloud_storage

    def update(self, command: ProjectUpdateCommand) -> None:
        """
        :raises UserNotFoundException:
        :raises ProjectNotFoundException:
        """
        logger.warning("Started updating project.")

        user: User = self._user_read_repository.get_by_id(id_=command.user_id)
        project: Project = self._project_read_repository.get_by_id(id_=command.project_id)

        if command.category_ids:
            self._check_category_ids(category_ids=command.category_ids)
        if command.funding_model_id:
            self._check_funding_model_exists(funding_model_id=command.funding_model_id)
        if command.steps:
            self._update_project_steps(project=project, steps=command.steps)
        if command.incubator:
            self._update_incubator(user=user, project=project, incubator_payload=command.incubator)

        plan_path: str | None = None
        if command.plan_file:
            if project.plan is None:
                plan_path = PathProvider.get_project_plan_path()
                self._upload_plan_file(plan_path=plan_path, plan_file=command.plan_file)
            else:
                self._upload_plan_file(plan_path=project.plan, plan_file=command.plan_file)

        payload: ProjectUpdatePayload = self._convert_command_to_payload(command=command, plan_path=plan_path)

        self._project_service.update(project=project, user=user, update_payload=payload)

        logger.info("Project updated successfully.")

    def _update_incubator(self, user: User, project: Project, incubator_payload: IncubatorUpdatePayload) -> None:
        incubators: list[ProjectIncubator] = self._incubator_read_repository.get_all(
            ProjectIncubatorFilter(project_id=Id(value=project.id))
        )
        if not incubators:
            logger.debug("Project has no incubator, started creating...")
            self._incubator_service.create(
                payload=IncubatorCreatePayload(
                    project_id=incubator_payload.project_id,
                    name=incubator_payload.name,
                    description=incubator_payload.description,
                )
            )
            logger.info("Incubator created successfully.")
        else:
            incubator: ProjectIncubator = incubators[0]
            logger.debug("Project has an incubator, started updating...")
            self._incubator_service.update(user=user, incubator=incubator, payload=incubator_payload)
            logger.info("Incubator updated successfully.")

    def _update_project_steps(self, project: Project, steps: list[ProjectStepCreateCommand]) -> None:
        self._project_step_service.check_project_max_steps_limit(project_steps=steps)
        self._project_step_service.delete_all_for_project(project=project)

        for step in steps:
            step_model: ProjectStep = self._project_step_service.create(
                paylaod=ProjectStepCreatePaylaod(
                    project_id=Id(value=project.id),
                    name=step.name,
                    description=step.description,
                    date=step.date,
                )
            )
            logger.debug(f"Step with id = {step_model.id} created successfully.")
        logger.info("All steps created successfully.")

    def _upload_plan_file(self, plan_path: str, plan_file: PdfFile) -> None:
        logger.debug("Updating: project_plan file.")
        self._cloud_storage.upload_file(CloudStorageUploadPayload(file_data=plan_file.value, file_path=plan_path))

    def _check_category_ids(self, category_ids: list[Id]) -> None:
        """:raises ProjectCategoryNotFoundException:"""
        logger.debug("Checking: categories exist.")

        categories: list[ProjectCategory] = self._project_category_read_repository.get_all(
            filter_=ProjectCategoryFilter(category_ids=category_ids)
        )
        existing_category_ids: list[Id] = [Id(value=i.id) for i in categories]
        for i in category_ids:
            if i not in existing_category_ids:
                raise ProjectCategoryNotFoundException(f"Category with id {i.value} not found.")

    def _check_funding_model_exists(self, funding_model_id: Id) -> None:
        """:raises FundingModelNotFoundException:"""
        logger.debug("Checking: funding model exists.")

        self._funding_model_read_repository.get_by_id(id_=funding_model_id)

    def _convert_command_to_payload(self, command: ProjectUpdateCommand, plan_path: str | None) -> ProjectUpdatePayload:
        return ProjectUpdatePayload(
            id_=command.project_id,
            name=command.name,
            description=command.description,
            goal_description=command.goal_description,
            category_ids=command.category_ids,
            funding_model_id=command.funding_model_id,
            stage=command.stage,
            goal_sum=command.goal_sum,
            deadline=command.deadline,
            plan_path=plan_path,
        )
