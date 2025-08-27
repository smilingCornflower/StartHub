from abc import ABC, abstractmethod

from domain.models.project_management.media import ProjectMedia
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import CursorPagination, OffsetPagination
from domain.value_objects.filter import ProjectMediaFilter
from domain.value_objects.project.media import ProjectMediaCreatePayload, ProjectMediaId, ProjectMediaUpdatePayload


class ProjectMediaReadRepository(AbstractReadRepository[ProjectMedia, ProjectMediaFilter, ProjectMediaId], ABC):
    @abstractmethod
    def get_by_id(self, id_: ProjectMediaId) -> ProjectMedia:
        pass

    @abstractmethod
    def get_all(
        self, filter_: ProjectMediaFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[ProjectMedia]:
        pass


class ProjectMediaWriteRepository(
    AbstractWriteRepository[ProjectMedia, ProjectMediaCreatePayload, ProjectMediaUpdatePayload, ProjectMediaId], ABC
):
    @abstractmethod
    def create(self, data: ProjectMediaCreatePayload) -> ProjectMedia:
        pass

    @abstractmethod
    def update(self, data: ProjectMediaUpdatePayload) -> ProjectMedia:
        pass

    @abstractmethod
    def delete_by_id(self, id_: ProjectMediaId) -> None:
        pass

    @abstractmethod
    def delete(self, project_media: ProjectMedia) -> None:
        pass
