from domain.constants import PROJECT_PLAN_PATH
from domain.exceptions.company import CompanyOwnershipRequiredException
from domain.exceptions.permissions import DeletePermissionDenied
from domain.exceptions.project_management import (
    ProjectPhoneAlreadyExistsException,
    ProjectSocialLinkAlreadyExistsException,
)
from domain.models.company import Company
from domain.models.project import Project, ProjectPhone, ProjectSocialLink, TeamMember
from domain.ports.cloud_storage import AbstractCloudStorage
from domain.repositories.company import CompanyReadRepository
from domain.repositories.project_management import (
    FundingModelReadRepository,
    ProjectCategoryReadRepository,
    ProjectPhoneReadRepository,
    ProjectPhoneWriteRepository,
    ProjectReadRepository,
    ProjectSocialLinkReadRepository,
    ProjectSocialLinkWriteRepository,
    ProjectWriteRepository,
    TeamMemberReadRepository,
    TeamMemberWriteRepository,
)
from domain.repositories.user import UserReadRepository
from domain.services.file import PdfService
from domain.value_objects.cloud_storage import CloudStorageCreateUrlPayload, CloudStorageUploadPayload
from domain.value_objects.common import Id
from domain.value_objects.filter import ProjectFilter, ProjectPhoneFilter, ProjectSocialLinkFilter
from domain.value_objects.project_management import (
    ProjectCreatePayload,
    ProjectPhoneCreatePayload,
    ProjectSocialLinkCreatePayload,
    ProjectUpdatePayload,
    TeamMemberCreatePayload,
)
from loguru import logger


class ProjectPhoneService:
    def __init__(
        self,
        project_phone_read_repository: ProjectPhoneReadRepository,
        project_phone_write_repository: ProjectPhoneWriteRepository,
    ):
        self._read_repository = project_phone_read_repository
        self._write_repository = project_phone_write_repository

    def create(self, payload: ProjectPhoneCreatePayload) -> ProjectPhone:
        """:raises ProjectPhoneAlreadyExistsException:"""

        filter_result: list[ProjectPhone] = self._read_repository.get_all(
            ProjectPhoneFilter(project_id=payload.project_id, number=payload.number)
        )
        if filter_result:
            raise ProjectPhoneAlreadyExistsException(
                f"This phone number is already assigned to the project with id = {payload.project_id}"
            )
        return self._write_repository.create(payload)


class ProjectSocialLinkService:
    def __init__(
        self,
        read_repository: ProjectSocialLinkReadRepository,
        write_repository: ProjectSocialLinkWriteRepository,
    ):
        self._read_repository = read_repository
        self._write_repository = write_repository

    def create(self, payload: ProjectSocialLinkCreatePayload) -> ProjectSocialLink:
        """:raises ProjectSocialLinkAlreadyExistsException:"""

        filter_result: list[ProjectSocialLink] = self._read_repository.get_all(
            ProjectSocialLinkFilter(project_id=payload.project_id, social_link=payload.social_link)
        )
        if filter_result:
            raise ProjectSocialLinkAlreadyExistsException(
                f"social_link: {payload.social_link} already exists for the project with id = {payload.project_id.value}."
            )
        return self._write_repository.create(payload)


class TamMemberService:
    def __init__(
        self,
        team_member_read_repository: TeamMemberReadRepository,
        team_member_write_repository: TeamMemberWriteRepository,
    ):
        self._team_member_read_repository = team_member_read_repository
        self._team_member_write_repository = team_member_write_repository

    def create(self, payload: TeamMemberCreatePayload) -> TeamMember:
        return self._team_member_write_repository.create(payload)


class ProjectService:
    def __init__(
        self,
        project_read_repository: ProjectReadRepository,
        project_write_repository: ProjectWriteRepository,
        project_category_read_repository: ProjectCategoryReadRepository,
        user_read_repository: UserReadRepository,
        funding_model_read_repository: FundingModelReadRepository,
        company_read_repository: CompanyReadRepository,
        cloud_storage: AbstractCloudStorage,
        pdf_service: PdfService,
    ):
        self._project_read_repository = project_read_repository
        self._project_write_repository = project_write_repository
        self._project_category_read_repository = project_category_read_repository
        self._user_read_repository = user_read_repository
        self._funding_model_read_repository = funding_model_read_repository
        self._company_read_repository = company_read_repository
        self._cloud_storage = cloud_storage
        self._pdf_service = pdf_service

    def get_by_id(self, id_: Id) -> Project:
        """:raises ProjectNotFoundException:"""
        return self._project_read_repository.get_by_id(id_=id_)

    def get(self, filter_: ProjectFilter) -> list[Project]:
        return self._project_read_repository.get_all(filter_=filter_)

    def get_plan_url(self, project_id: Id) -> str:
        plan_path = self._generate_plan_path(project_id)
        return self._cloud_storage.create_url(payload=CloudStorageCreateUrlPayload(file_path=plan_path))

    def _generate_plan_path(self, project_id: Id) -> str:
        return f"{PROJECT_PLAN_PATH}/{project_id.value}.pdf"

    def create(self, payload: ProjectCreatePayload) -> Project:
        """
        :raises ProjectCategoryNotFoundException:
        :raises UserNotFoundException:
        :raises FundingModelNotFoundException:
        :raises CompanyNotFoundException:
        :raises CompanyOwnershipRequiredException:
        """
        self._project_category_read_repository.get_by_id(payload.category_id)
        self._user_read_repository.get_by_id(payload.creator_id)
        self._funding_model_read_repository.get_by_id(payload.funding_model_id)

        company: Company = self._company_read_repository.get_by_id(payload.company_id)

        if company.representative_id != payload.creator_id.value:
            logger.debug(f"Company representative: {company.representative_id}; user_id: {payload.creator_id.value}")
            raise CompanyOwnershipRequiredException("User is not the representative of this company.")

        project: Project = self._project_write_repository.create(payload)
        logger.info("Project created successfully.")
        project_plan_path: str = self._generate_plan_path(project_id=Id(value=project.id))
        uploaded_path: str = self._cloud_storage.upload_file(
            CloudStorageUploadPayload(file_data=payload.project_plan_data, file_path=project_plan_path)
        )
        logger.debug("Project pdf uploaded.")

        assert project_plan_path == uploaded_path
        self._project_write_repository.update(ProjectUpdatePayload(id_=Id(value=project.id), plan=project_plan_path))
        logger.debug("Project.plan field was updated.")

        return project

    def update(self, payload: ProjectUpdatePayload, user_id: Id) -> Project:
        """
        :raises ProjectCategoryNotFoundException:
        :raises FundingModelNotFoundException:
        :raises DeletePermissionDenied:
        """

        project: Project = self._project_read_repository.get_by_id(id_=payload.id_)
        if project.creator_id != user_id.value:
            raise DeletePermissionDenied("Permission denied: Only project owners can update projects")

        if payload.category_id:
            self._project_category_read_repository.get_by_id(payload.category_id)
        if payload.funding_model_id:
            self._funding_model_read_repository.get_by_id(payload.funding_model_id)

        project_updated: Project = self._project_write_repository.update(payload)
        return project_updated

    def delete(self, project_id: Id, user_id: Id) -> None:
        """
        :raises DeletePermissionDenied:
        """
        project: Project = self._project_read_repository.get_by_id(id_=project_id)
        if project.creator_id != user_id.value:
            raise DeletePermissionDenied("Permission denied: Only project owners can delete projects")

        self._project_write_repository.delete(id_=project_id)
