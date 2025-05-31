from domain.exceptions.company import CompanyOwnershipRequiredException
from domain.exceptions.permissions import DeletePermissionDenied
from domain.models.company import Company
from domain.models.project import Project
from domain.repositories.company import CompanyReadRepository
from domain.repositories.funding_model import FundingModelReadRepository
from domain.repositories.project import ProjectReadRepository, ProjectWriteRepository
from domain.repositories.project_category import ProjectCategoryReadRepository
from domain.repositories.user import UserReadRepository
from domain.value_objects.common import Id
from domain.value_objects.filter import ProjectFilter
from domain.value_objects.project import ProjectCreatePayload, ProjectUpdatePayload
from loguru import logger


class ProjectService:
    def __init__(
        self,
        project_read_repository: ProjectReadRepository,
        project_write_repository: ProjectWriteRepository,
        project_category_read_repository: ProjectCategoryReadRepository,
        user_read_repository: UserReadRepository,
        funding_model_read_repository: FundingModelReadRepository,
        company_read_repository: CompanyReadRepository,
    ):
        self._project_read_repository = project_read_repository
        self._project_write_repository = project_write_repository
        self._project_category_read_repository = project_category_read_repository
        self._user_read_repository = user_read_repository
        self._funding_model_read_repository = funding_model_read_repository
        self._company_read_repository = company_read_repository

    def get_by_id(self, id_: Id) -> Project:
        """:raises ProjectNotFoundException:"""
        return self._project_read_repository.get_by_id(id_=id_)

    def get(self, filter_: ProjectFilter) -> list[Project]:
        return self._project_read_repository.get_all(filter_=filter_)

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
        return project

    def update(self, payload: ProjectUpdatePayload, user_id: Id) -> Project:
        """
        :raises ProjectCategoryNotFoundException:
        :raises FundingModelNotFoundException:
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
