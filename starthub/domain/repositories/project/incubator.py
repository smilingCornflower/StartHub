from abc import ABC, abstractmethod

from domain.models.project_management.incubator import ProjectIncubator
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Pagination
from domain.value_objects.filter import ProjectIncubatorFilter
from domain.value_objects.project.incubator import IncubatorCreatePayload, IncubatorId, IncubatorUpdatePayload


class PojectIncubatorReadRepository(AbstractReadRepository[ProjectIncubator, ProjectIncubatorFilter, IncubatorId], ABC):
    @abstractmethod
    def get_by_id(self, id_: IncubatorId) -> ProjectIncubator:
        pass

    @abstractmethod
    def get_all(self, filter_: ProjectIncubatorFilter, pagination: Pagination | None = None) -> list[ProjectIncubator]:
        pass


class ProjectIncubatorWriteRepository(
    AbstractWriteRepository[ProjectIncubator, IncubatorCreatePayload, IncubatorUpdatePayload, IncubatorId], ABC
):
    @abstractmethod
    def create(self, data: IncubatorCreatePayload) -> ProjectIncubator:
        pass

    @abstractmethod
    def update(self, data: IncubatorUpdatePayload) -> ProjectIncubator:
        pass

    @abstractmethod
    def delete_by_id(self, id_: IncubatorId) -> None:
        pass
