from abc import ABC, abstractmethod

from domain.models.project_management.crowdfunding import ProjectCrowdfunding
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Pagination
from domain.value_objects.filter import ProjectCrowdfundingFilter
from domain.value_objects.project.crowdfunding import (
    ProjectCrowdfundingCreatePayload,
    ProjectCrowdfundingId,
    ProjectCrowdfundingUpdatePayload,
)


class CrowdfundingReadRepository(
    AbstractReadRepository[ProjectCrowdfunding, ProjectCrowdfundingFilter, ProjectCrowdfundingId], ABC
):
    @abstractmethod
    def get_by_id(self, id_: ProjectCrowdfundingId) -> ProjectCrowdfunding:
        pass

    @abstractmethod
    def get_all(
        self, filter_: ProjectCrowdfundingFilter, pagination: Pagination | None = None
    ) -> list[ProjectCrowdfunding]:
        pass


class CrowdundingWriteRepository(
    AbstractWriteRepository[
        ProjectCrowdfunding, ProjectCrowdfundingCreatePayload, ProjectCrowdfundingUpdatePayload, ProjectCrowdfundingId
    ],
    ABC,
):
    @abstractmethod
    def create(self, data: ProjectCrowdfundingCreatePayload) -> ProjectCrowdfunding:
        pass

    @abstractmethod
    def update(self, data: ProjectCrowdfundingUpdatePayload) -> ProjectCrowdfunding:
        pass

    @abstractmethod
    def delete_by_id(self, id_: ProjectCrowdfundingId) -> None:
        pass
