from application.converters.resposne_converters.project import project_to_dto
from application.dto.project import ProjectDto
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
from domain.models.project import Project, ProjectImage
from domain.models.project_category import ProjectCategory
from domain.models.user import User
from domain.ports.cloud_storage import AbstractCloudStorage
from domain.repositories.company import CompanyReadRepository
from domain.repositories.country import CountryReadRepository
from domain.repositories.geo.city import CityReadRepository
from domain.repositories.geo.region import RegionReadRepository
from domain.repositories.project_management import (
    FundingModelReadRepository,
    ProjectCategoryReadRepository,
    ProjectImageReadRepository,
    ProjectReadRepository,
)
from domain.repositories.user import UserReadRepository
from domain.repositories.user_favorite import UserFavoriteReadRepository
from domain.services.project_management.project import ProjectService
from domain.utils.path_provider import PathProvider
from domain.value_objects.cloud_storage import CloudStorageCreateUrlPayload, CloudStorageUploadPayload
from domain.value_objects.common import Id, OffsetPagination, Pagination
from domain.value_objects.company import BusinessNumber
from domain.value_objects.country import CountryCode
from domain.value_objects.file import PdfFile
from domain.value_objects.filter import (
    CompanyFilter,
    CountryFilter,
    ProjectCategoryFilter,
    ProjectFilter,
    ProjectImageFilter,
)
from domain.value_objects.geo import CityId, RegionId
from domain.value_objects.project_management import (
    ProjectCreateCommand,
    ProjectCreatePayload,
    ProjectStatus,
    ProjectUpdateCommand,
    ProjectUpdatePayload,
)
from domain.value_objects.search import ProjectSearchParams
from infrastructure.event_bus import EventBus
from infrastructure.services.project_search import ProjectSearchService
from loguru import logger


class ProjectCreateAppService(AbstractAppService):
    def __init__(
        self,
        project_service: ProjectService,
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
        self._cloud_storage = cloud_storage
        self._user_read_repository = user_read_repository
        self._funding_model_read_repository = funding_model_read_repository
        self._company_read_repository = company_read_repository
        self._country_read_repository = country_read_repository
        self._project_category_read_repository = project_category_read_repository
        self._city_read_repository = city_read_repository
        self._region_read_repository = region_read_repository

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

    def create(self, command: ProjectCreateCommand) -> Project:
        logger.warning("Started creating project.")
        self._validate_dependencies(command=command)

        plan_path: str = self._upload_plan(plan_file=command.plan_file)
        create_payload: ProjectCreatePayload = self._convert_command_to_payload(command=command, plan_path=plan_path)

        with transaction.atomic():
            project: Project = self._project_service.create(payload=create_payload)

            event = ProjectCreatedEvent(project_id=Id(value=project.id), command=command)
            EventBus().publish(event)

        return project


class ProjectGetAppService(AbstractAppService):
    def __init__(
        self,
        project_read_repository: ProjectReadRepository,
        project_image_read_repository: ProjectImageReadRepository,
        project_category_read_repository: ProjectCategoryReadRepository,
        user_favorite_read_repository: UserFavoriteReadRepository,
        project_search_service: ProjectSearchService,
        cloud_storage: AbstractCloudStorage,
    ):
        self._project_read_repository = project_read_repository
        self._project_image_read_repository = project_image_read_repository
        self._project_category_read_repository = project_category_read_repository
        self._user_favorite_read_repository = user_favorite_read_repository
        self._project_search_service = project_search_service
        self._cloud_storage = cloud_storage

    def get(self, filter_: ProjectFilter, pagination: Pagination, user_id: Id | None = None) -> list[ProjectDto]:
        projects: list[Project] = self._project_read_repository.get_all(filter_=filter_, pagination=pagination)
        logger.debug(f"Found {len(projects)} projectes.")

        return [self._create_dto(project=project, user_id=user_id) for project in projects]

    def get_by_id(self, project_id: Id, user_id: Id | None = None) -> ProjectDto:
        project: Project = self._project_read_repository.get_by_id(id_=project_id)
        logger.debug(f"Project with id = {project_id.value} found.")

        return self._create_dto(project=project, user_id=user_id)

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
        user_read_repository: UserReadRepository,
        project_read_repository: ProjectReadRepository,
        project_category_read_repository: ProjectCategoryReadRepository,
        funding_model_read_repository: FundingModelReadRepository,
        cloud_storage: AbstractCloudStorage,
    ):
        self._project_service = project_service
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
            category_ids=command.category_ids,
            funding_model_id=command.funding_model_id,
            stage=command.stage,
            goal_sum=command.goal_sum,
            deadline=command.deadline,
            plan_path=plan_path,
        )
