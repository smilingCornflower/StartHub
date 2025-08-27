from abc import ABC, abstractmethod

from domain.models.project_management.project_file import ProjectFile
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import CursorPagination, OffsetPagination
from domain.value_objects.filter import ProjectFileFilter
from domain.value_objects.project.project_file import ProjectFileCreatePayload, ProjectFileId, ProjectFileUpdatePayload


class ProjectFileReadRepository(AbstractReadRepository[ProjectFile, ProjectFileFilter, ProjectFileId], ABC):
    @abstractmethod
    def get_by_id(self, id_: ProjectFileId) -> ProjectFile:
        pass

    @abstractmethod
    def get_all(
        self, filter_: ProjectFileFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[ProjectFile]:
        pass


class ProjectFileWriteRepository(
    AbstractWriteRepository[ProjectFile, ProjectFileCreatePayload, ProjectFileUpdatePayload, ProjectFileId], ABC
):
    @abstractmethod
    def create(self, data: ProjectFileCreatePayload) -> ProjectFile:
        pass

    @abstractmethod
    def update(self, data: ProjectFileUpdatePayload) -> ProjectFile:
        pass

    @abstractmethod
    def delete_by_id(self, id_: ProjectFileId) -> None:
        pass

    @abstractmethod
    def delete(self, project_file: ProjectFile) -> None:
        pass
