from abc import ABC, abstractmethod

from domain.models import ProjectStage
from domain.ports.repository import AbstractReadRepository
from domain.value_objects.common import CursorPagination, OffsetPagination
from domain.value_objects.filter import ProjectStageFilter
from domain.value_objects.project.stage import ProjectStageId


class ProjectStageReadRepository(AbstractReadRepository[ProjectStage, ProjectStageFilter, ProjectStageId], ABC):
    @abstractmethod
    def get_by_id(self, id_: ProjectStageId) -> ProjectStage:
        pass

    @abstractmethod
    def get_all(
        self, filter_: ProjectStageFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[ProjectStage]:
        pass
