from abc import ABC, abstractmethod

from domain.models.project_management.social_link import ProjectSocialLink
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import CursorPagination, Id, OffsetPagination
from domain.value_objects.filter import ProjectSocialLinkFilter
from domain.value_objects.project.social_link import ProjectSocialLinkCreatePayload, ProjectSocialLinkUpdatePayload


class ProjectSocialLinkReadRepository(AbstractReadRepository[ProjectSocialLink, ProjectSocialLinkFilter, Id], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> ProjectSocialLink:
        pass

    @abstractmethod
    def get_all(
        self, filter_: ProjectSocialLinkFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[ProjectSocialLink]:
        pass


class ProjectSocialLinkWriteRepository(
    AbstractWriteRepository[ProjectSocialLink, ProjectSocialLinkCreatePayload, ProjectSocialLinkUpdatePayload, Id], ABC
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
