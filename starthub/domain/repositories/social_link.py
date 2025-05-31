from abc import ABC, abstractmethod

from domain.models.project import ProjectSocialLink
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Id
from domain.value_objects.filter import ProjectSocialLinkFilter
from domain.value_objects.project_social_link import ProjectSocialLinkCreatePayload, ProjectSocialLinkUpdatePayload


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
