from abc import ABC, abstractmethod

from domain.models.project_management.report import ProjectReport
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Pagination
from domain.value_objects.filter import ProjectReportFilter
from domain.value_objects.project.report import ProjectReportCreatePayload, ProjectReportId, ProjectUpdatePayload


class ProjectReportReadRepository(AbstractReadRepository[ProjectReport, ProjectReportFilter, ProjectReportId], ABC):
    @abstractmethod
    def get_by_id(self, id_: ProjectReportId) -> ProjectReport:
        pass

    @abstractmethod
    def get_all(self, filter_: ProjectReportFilter, pagination: Pagination | None = None) -> list[ProjectReport]:
        pass


class ProjectReportWriteRepository(
    AbstractWriteRepository[ProjectReport, ProjectReportCreatePayload, ProjectUpdatePayload, ProjectReportId], ABC
):
    @abstractmethod
    def create(self, data: ProjectReportCreatePayload) -> ProjectReport:
        pass

    @abstractmethod
    def update(self, data: ProjectUpdatePayload) -> ProjectReport:
        pass

    @abstractmethod
    def delete_by_id(self, id_: ProjectReportId) -> None:
        pass
