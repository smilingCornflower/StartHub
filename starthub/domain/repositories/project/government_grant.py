from abc import ABC, abstractmethod

from domain.models.project_management.government_grant import ProjectGovernmentGrant
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Pagination
from domain.value_objects.filter import ProjectGovernmentGrantFilter
from domain.value_objects.project.government_grant import (
    ProjectGovernmentGrantId,
    ProjectGovernmentGrantUpdatePayload,
    ProjectGoverntmentGrantCreatePayload,
)


class ProjectGovernmentGrantReadRepository(
    AbstractReadRepository[ProjectGovernmentGrant, ProjectGovernmentGrantFilter, ProjectGovernmentGrantId], ABC
):
    @abstractmethod
    def get_by_id(self, id_: ProjectGovernmentGrantId) -> ProjectGovernmentGrant:
        pass

    @abstractmethod
    def get_all(
        self, filter_: ProjectGovernmentGrantFilter, pagination: Pagination | None = None
    ) -> list[ProjectGovernmentGrant]:
        pass


class ProjectGovernmentGrantWriteRepository(
    AbstractWriteRepository[
        ProjectGovernmentGrant,
        ProjectGoverntmentGrantCreatePayload,
        ProjectGovernmentGrantUpdatePayload,
        ProjectGovernmentGrantId,
    ],
    ABC,
):
    @abstractmethod
    def create(self, data: ProjectGoverntmentGrantCreatePayload) -> ProjectGovernmentGrant:
        pass

    @abstractmethod
    def update(self, data: ProjectGovernmentGrantUpdatePayload) -> ProjectGovernmentGrant:
        pass

    @abstractmethod
    def delete_by_id(self, id_: ProjectGovernmentGrantId) -> None:
        pass

    @abstractmethod
    def delete(self, government_grant: ProjectGovernmentGrant) -> None:
        pass
