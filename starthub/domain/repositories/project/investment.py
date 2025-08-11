from abc import ABC, abstractmethod

from domain.models.project_management.investment import ProjectInvestment
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Pagination
from domain.value_objects.filter import ProjectInvestmentFilter
from domain.value_objects.project.investment import (
    ProjectInvestmentCreatePayload,
    ProjectInvestmentId,
    ProjectInvestmentUpdatePayload,
)


class ProjectInestmentReadRepository(
    AbstractReadRepository[ProjectInvestment, ProjectInvestmentFilter, ProjectInvestmentId], ABC
):
    @abstractmethod
    def get_by_id(self, id_: ProjectInvestmentId) -> ProjectInvestment:
        pass

    @abstractmethod
    def get_all(
        self, filter_: ProjectInvestmentFilter, pagination: Pagination | None = None
    ) -> list[ProjectInvestment]:
        pass


class ProjectInvestmentWriteRepository(
    AbstractWriteRepository[
        ProjectInvestment, ProjectInvestmentCreatePayload, ProjectInvestmentUpdatePayload, ProjectInvestmentId
    ],
    ABC,
):
    @abstractmethod
    def create(self, data: ProjectInvestmentCreatePayload) -> ProjectInvestment:
        pass

    @abstractmethod
    def update(self, data: ProjectInvestmentUpdatePayload) -> ProjectInvestment:
        pass

    @abstractmethod
    def delete_by_id(self, id_: ProjectInvestmentId) -> None:
        pass
