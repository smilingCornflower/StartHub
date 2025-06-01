from abc import ABC, abstractmethod

from domain.models.funding_model import FundingModel
from domain.models.project import Project, ProjectPhone, ProjectSocialLink, TeamMember
from domain.models.project_category import ProjectCategory
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Id, Slug
from domain.value_objects.filter import (
    FundingModelFilter,
    ProjectCategoryFilter,
    ProjectFilter,
    ProjectPhoneFilter,
    ProjectSocialLinkFilter,
    TeamMemberFilter,
)
from domain.value_objects.project_management import (
    ProjectCategoryCreatePayload,
    ProjectCategoryUpdatePayload,
    ProjectCreatePayload,
    ProjectPhoneCreatePayload,
    ProjectPhoneUpdatePayload,
    ProjectSocialLinkCreatePayload,
    ProjectSocialLinkUpdatePayload,
    ProjectUpdatePayload,
    TeamMemberCreatePayload,
    TeamMemberUpdatePayload,
)


class ProjectCategoryReadRepository(AbstractReadRepository[ProjectCategory, ProjectCategoryFilter], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> ProjectCategory:
        """:raises ProjectCategoryNotFoundException:"""
        pass

    @abstractmethod
    def get_all(self, filter_: ProjectCategoryFilter) -> list[ProjectCategory]:
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
    def delete(self, id_: Id) -> None:
        """:raises ProjectCategoryNotFoundException:"""
        pass


class ProjectPhoneReadRepository(AbstractReadRepository[ProjectPhone, ProjectPhoneFilter], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> ProjectPhone:
        pass

    @abstractmethod
    def get_all(self, filter_: ProjectPhoneFilter) -> list[ProjectPhone]:
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
    def delete(self, id_: Id) -> None:
        pass


class ProjectSocialLinkReadRepository(AbstractReadRepository[ProjectSocialLink, ProjectSocialLinkFilter], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> ProjectSocialLink:
        pass

    @abstractmethod
    def get_all(self, filter_: ProjectSocialLinkFilter) -> list[ProjectSocialLink]:
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
    def delete(self, id_: Id) -> None:
        pass


class TeamMemberReadRepository(AbstractReadRepository[TeamMember, TeamMemberFilter], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> TeamMember:
        pass

    @abstractmethod
    def get_all(self, filter_: TeamMemberFilter) -> list[TeamMember]:
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
    def delete(self, id_: Id) -> None:
        pass


class ProjectReadRepository(AbstractReadRepository[Project, ProjectFilter], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> Project:
        """:raises ProjectNotFoundException:"""
        pass

    @abstractmethod
    def get_all(self, filter_: ProjectFilter) -> list[Project]:
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
    def delete(self, id_: Id) -> None:
        """:raises ProjectNotFoundException:"""
        pass


class FundingModelReadRepository(AbstractReadRepository[FundingModel, FundingModelFilter], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> FundingModel:
        """:raises FundingModelNotFoundException:"""
        pass

    @abstractmethod
    def get_all(self, filter_: FundingModelFilter) -> list[FundingModel]:
        pass
