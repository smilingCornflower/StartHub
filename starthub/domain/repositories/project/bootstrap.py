from abc import ABC, abstractmethod

from domain.models.project_management.bootstrap import ProjectBootstrap
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Pagination
from domain.value_objects.filter import ProjectBootstrapFilter
from domain.value_objects.project.bootstrap import (
    ProjectBootstrapCreatePayload,
    ProjectBootstrapId,
    ProjectBootstrapUpdatePayload,
)


class ProjectBootstrapReadRepository(
    AbstractReadRepository[ProjectBootstrap, ProjectBootstrapFilter, ProjectBootstrapId], ABC
):
    @abstractmethod
    def get_by_id(self, id_: ProjectBootstrapId) -> ProjectBootstrap:
        pass

    @abstractmethod
    def get_all(self, filter_: ProjectBootstrapFilter, pagination: Pagination | None = None) -> list[ProjectBootstrap]:
        pass


class ProjectBootstrapWriteRepository(
    AbstractWriteRepository[
        ProjectBootstrap, ProjectBootstrapCreatePayload, ProjectBootstrapUpdatePayload, ProjectBootstrapId
    ],
    ABC,
):
    @abstractmethod
    def create(self, data: ProjectBootstrapCreatePayload) -> ProjectBootstrap:
        pass

    @abstractmethod
    def update(self, data: ProjectBootstrapUpdatePayload) -> ProjectBootstrap:
        pass

    @abstractmethod
    def delete_by_id(self, id_: ProjectBootstrapId) -> None:
        pass

    @abstractmethod
    def delete(self, bootsrtap: ProjectBootstrap) -> None:
        pass
