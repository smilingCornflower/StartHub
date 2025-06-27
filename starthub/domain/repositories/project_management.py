from abc import ABC, abstractmethod

from domain.models.funding_model import FundingModel
from domain.models.project import Project, ProjectImage, ProjectPhone, ProjectSocialLink, TeamMember
from domain.models.project_category import ProjectCategory
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Id, Pagination, Slug
from domain.value_objects.filter import (
    FundingModelFilter,
    ProjectCategoryFilter,
    ProjectFilter,
    ProjectImageFilter,
    ProjectPhoneFilter,
    ProjectSocialLinkFilter,
    TeamMemberFilter,
)
from domain.value_objects.project_management import (
    ProjectCategoryCreatePayload,
    ProjectCategoryUpdatePayload,
    ProjectCreatePayload,
    ProjectImageCreatePayload,
    ProjectImageDeletePayload,
    ProjectImageUpdatePayload,
    ProjectPhoneCreatePayload,
    ProjectPhoneUpdatePayload,
    ProjectSocialLinkCreatePayload,
    ProjectSocialLinkUpdatePayload,
    ProjectUpdatePayload,
    TeamMemberCreatePayload,
    TeamMemberUpdatePayload,
)


# noinspection DuplicatedCode
class ProjectCategoryReadRepository(AbstractReadRepository[ProjectCategory, ProjectCategoryFilter], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> ProjectCategory:
        """:raises ProjectCategoryNotFoundException:"""
        pass

    @abstractmethod
    def get_all(self, filter_: ProjectCategoryFilter, pagination: Pagination | None = None) -> list[ProjectCategory]:
        pass


class ProjectCategoryWriteRepository(
    AbstractWriteRepository[ProjectCategory, ProjectCategoryCreatePayload, ProjectCategoryUpdatePayload], ABC
):
    @abstractmethod
    def create(self, data: ProjectCategoryCreatePayload) -> ProjectCategory:
        pass

    @abstractmethod
    def update(self, data: ProjectCategoryUpdatePayload) -> ProjectCategory:
        """:raises ProjectCategoryNotFoundException:"""
        pass

    @abstractmethod
    def delete_by_id(self, id_: Id) -> None:
        """:raises ProjectCategoryNotFoundException:"""
        pass


class ProjectPhoneReadRepository(AbstractReadRepository[ProjectPhone, ProjectPhoneFilter], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> ProjectPhone:
        pass

    @abstractmethod
    def get_all(self, filter_: ProjectPhoneFilter, pagination: Pagination | None = None) -> list[ProjectPhone]:
        pass


class ProjectPhoneWriteRepository(
    AbstractWriteRepository[ProjectPhone, ProjectPhoneCreatePayload, ProjectPhoneUpdatePayload], ABC
):
    @abstractmethod
    def create(self, data: ProjectPhoneCreatePayload) -> ProjectPhone:
        pass

    @abstractmethod
    def update(self, data: ProjectPhoneUpdatePayload) -> ProjectPhone:
        pass

    @abstractmethod
    def delete_by_id(self, id_: Id) -> None:
        pass


# noinspection DuplicatedCode
class ProjectSocialLinkReadRepository(AbstractReadRepository[ProjectSocialLink, ProjectSocialLinkFilter], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> ProjectSocialLink:
        pass

    @abstractmethod
    def get_all(
        self, filter_: ProjectSocialLinkFilter, pagination: Pagination | None = None
    ) -> list[ProjectSocialLink]:
        pass


class ProjectSocialLinkWriteRepository(
    AbstractWriteRepository[ProjectSocialLink, ProjectSocialLinkCreatePayload, ProjectSocialLinkUpdatePayload], ABC
):
    @abstractmethod
    def create(self, data: ProjectSocialLinkCreatePayload) -> ProjectSocialLink:
        pass

    @abstractmethod
    def update(self, data: ProjectSocialLinkUpdatePayload) -> ProjectSocialLink:
        pass

    @abstractmethod
    def delete_by_id(self, id_: Id) -> None:
        pass


class TeamMemberReadRepository(AbstractReadRepository[TeamMember, TeamMemberFilter], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> TeamMember:
        pass

    @abstractmethod
    def get_all(self, filter_: TeamMemberFilter, pagination: Pagination | None = None) -> list[TeamMember]:
        pass


class TeamMemberWriteRepository(
    AbstractWriteRepository[TeamMember, TeamMemberCreatePayload, TeamMemberUpdatePayload], ABC
):
    @abstractmethod
    def create(self, data: TeamMemberCreatePayload) -> TeamMember:
        pass

    @abstractmethod
    def update(self, data: TeamMemberUpdatePayload) -> TeamMember:
        pass

    @abstractmethod
    def delete_by_id(self, id_: Id) -> None:
        pass


# noinspection DuplicatedCode
class ProjectReadRepository(AbstractReadRepository[Project, ProjectFilter], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> Project:
        """:raises ProjectNotFoundException:"""
        pass

    @abstractmethod
    def get_all(self, filter_: ProjectFilter, pagination: Pagination | None = None) -> list[Project]:
        pass

    @abstractmethod
    def get_by_slug(self, slug: Slug) -> Project:
        """:raises ProjectNotFoundException:"""
        pass


class ProjectWriteRepository(AbstractWriteRepository[Project, ProjectCreatePayload, ProjectUpdatePayload], ABC):
    @abstractmethod
    def create(self, data: ProjectCreatePayload) -> Project:
        pass

    @abstractmethod
    def update(self, data: ProjectUpdatePayload) -> Project:
        """:raises ProjectNotFoundException:"""
        pass

    @abstractmethod
    def delete_by_id(self, id_: Id) -> None:
        """:raises ProjectNotFoundException:"""
        pass


class FundingModelReadRepository(AbstractReadRepository[FundingModel, FundingModelFilter], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> FundingModel:
        """:raises FundingModelNotFoundException:"""
        pass

    @abstractmethod
    def get_all(self, filter_: FundingModelFilter, pagination: Pagination | None = None) -> list[FundingModel]:
        pass


# noinspection DuplicatedCode
class ProjectImageReadRepository(AbstractReadRepository[ProjectImage, ProjectImageFilter], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> ProjectImage:
        """:raises ProjectPhotoNotFoundException:"""
        pass

    @abstractmethod
    def get_all(self, filter_: ProjectImageFilter, pagination: Pagination | None = None) -> list[ProjectImage]:
        pass

    @abstractmethod
    def get_images_count_for_project(self, project_id: Id) -> int:
        pass


class ProjectImageWriteRepository(
    AbstractWriteRepository[ProjectImage, ProjectImageCreatePayload, ProjectImageUpdatePayload], ABC
):
    @abstractmethod
    def create(self, data: ProjectImageCreatePayload) -> ProjectImage:
        pass

    @abstractmethod
    def update(self, data: ProjectImageUpdatePayload) -> ProjectImage:
        pass

    @abstractmethod
    def delete_by_id(self, id_: Id) -> None:
        pass

    @abstractmethod
    def delete(self, data: ProjectImageDeletePayload) -> None:
        pass
