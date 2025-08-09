from abc import ABC, abstractmethod

from domain.models.project_management.accelerator import ProjectAccelerator
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Pagination
from domain.value_objects.filter import ProjectAcceleratorFilter
from domain.value_objects.project.accelerator import (
    AcceleratorId,
    ProjectAcceleratorCreatePayload,
    ProjectAcceleratorUpdatePayload,
)


class ProjectAcceleratorReadRepository(
    AbstractReadRepository[ProjectAccelerator, ProjectAcceleratorFilter, AcceleratorId], ABC
):
    @abstractmethod
    def get_by_id(self, id_: AcceleratorId) -> ProjectAccelerator:
        pass

    @abstractmethod
    def get_all(
        self, filter_: ProjectAcceleratorFilter, pagination: Pagination | None = None
    ) -> list[ProjectAccelerator]:
        pass


class ProjectAcceleratorWriteRepository(
    AbstractWriteRepository[
        ProjectAccelerator, ProjectAcceleratorCreatePayload, ProjectAcceleratorUpdatePayload, AcceleratorId
    ],
    ABC,
):
    @abstractmethod
    def create(self, data: ProjectAcceleratorCreatePayload) -> ProjectAccelerator:
        pass

    @abstractmethod
    def update(self, data: ProjectAcceleratorUpdatePayload) -> ProjectAccelerator:
        pass

    @abstractmethod
    def delete_by_id(self, id_: AcceleratorId) -> None:
        pass

    @abstractmethod
    def delete(self, accelerator: ProjectAccelerator) -> None:
        pass
