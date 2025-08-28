from abc import ABC, abstractmethod

from domain.models import ProjectStage
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import CursorPagination, OffsetPagination
from domain.value_objects.filter import ProjectStageFilter
from domain.value_objects.project.stage import ProjectStageCreatePayload, ProjectStageId, ProjectStageUpdatePayload


class ProjectStageReadRepository(AbstractReadRepository[ProjectStage, ProjectStageFilter, ProjectStageId], ABC):
    @abstractmethod
    def get_by_id(self, id_: ProjectStageId) -> ProjectStage:
        pass

    @abstractmethod
    def get_all(
        self, filter_: ProjectStageFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[ProjectStage]:
        pass


class ProjectStageWriteRepository(
    AbstractWriteRepository[ProjectStage, ProjectStageCreatePayload, ProjectStageUpdatePayload, ProjectStageId], ABC
):
    @abstractmethod
    def create(self, data: ProjectStageCreatePayload) -> ProjectStage:
        pass

    @abstractmethod
    def update(self, data: ProjectStageUpdatePayload) -> ProjectStage:
        pass

    @abstractmethod
    def delete_by_id(self, id_: ProjectStageId) -> None:
        pass
