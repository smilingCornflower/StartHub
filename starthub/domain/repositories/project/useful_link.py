from abc import ABC, abstractmethod

from domain.models.project_management.useful_link import ProjectUsefulLink
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Pagination
from domain.value_objects.filter import ProjectUsefulLinkFilter
from domain.value_objects.project.useful_link import UsefulLinkCreatePayload, UsefulLinkId, UsefulLinkUpdatePayload


class ProjectUsefulLinkReadRepository(
    AbstractReadRepository[ProjectUsefulLink, ProjectUsefulLinkFilter, UsefulLinkId], ABC
):
    @abstractmethod
    def get_by_id(self, id_: UsefulLinkId) -> ProjectUsefulLink:
        pass

    @abstractmethod
    def get_all(
        self, filter_: ProjectUsefulLinkFilter, pagination: Pagination | None = None
    ) -> list[ProjectUsefulLink]:
        pass


class ProjectUsefulLinkWriteRepository(
    AbstractWriteRepository[ProjectUsefulLink, UsefulLinkCreatePayload, UsefulLinkUpdatePayload, UsefulLinkId], ABC
):
    @abstractmethod
    def create(self, data: UsefulLinkCreatePayload) -> ProjectUsefulLink:
        pass

    @abstractmethod
    def update(self, data: UsefulLinkUpdatePayload) -> ProjectUsefulLink:
        pass

    @abstractmethod
    def delete_by_id(self, id_: UsefulLinkId) -> None:
        pass

    @abstractmethod
    def delete(self, link: ProjectUsefulLink) -> None:
        pass
