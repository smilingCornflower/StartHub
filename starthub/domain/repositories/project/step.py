from abc import ABC, abstractmethod

from domain.models.project_management.step import ProjectStep
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Id, Pagination
from domain.value_objects.filter import ProjectStepFilter
from domain.value_objects.project.step import ProjectStepCreatePaylaod, ProjectStepId, ProjectStepUpdatePayload


class ProjectStepReadRepository(AbstractReadRepository[ProjectStep, ProjectStepFilter, ProjectStepId], ABC):
    @abstractmethod
    def get_by_id(self, id_: ProjectStepId) -> ProjectStep:
        pass

    @abstractmethod
    def get_all(self, filter_: ProjectStepFilter, pagination: Pagination | None = None) -> list[ProjectStep]:
        pass


class ProjectStepWriteRepository(
    AbstractWriteRepository[ProjectStep, ProjectStepCreatePaylaod, ProjectStepUpdatePayload, Id], ABC
):
    @abstractmethod
    def create(self, data: ProjectStepCreatePaylaod) -> ProjectStep:
        pass

    @abstractmethod
    def update(self, data: ProjectStepUpdatePayload) -> ProjectStep:
        pass

    @abstractmethod
    def delete_by_id(self, id_: Id) -> None:
        pass
