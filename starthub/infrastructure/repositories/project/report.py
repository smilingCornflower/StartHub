from domain.models.project_management.report import ProjectReport
from domain.repositories.project.report import ProjectReportReadRepository, ProjectReportWriteRepository
from domain.value_objects.common import Pagination
from domain.value_objects.filter import ProjectReportFilter
from domain.value_objects.project.report import ProjectReportCreatePayload, ProjectReportId, ProjectUpdatePayload


class DjProjectReportReadRepository(ProjectReportReadRepository):
    def get_by_id(self, id_: ProjectReportId) -> ProjectReport:
        raise NotImplementedError("The method get_by_id() is not implemented yet.")

    def get_all(self, filter_: ProjectReportFilter, pagination: Pagination | None = None) -> list[ProjectReport]:
        raise NotImplementedError("The method get_all() is not implemented yet.")


class DjProjectReportWriteRepository(ProjectReportWriteRepository):
    def create(self, data: ProjectReportCreatePayload) -> ProjectReport:
        return ProjectReport.objects.create(
            project_id=data.project_id.value,
            content=data.content.value,
        )

    def update(self, data: ProjectUpdatePayload) -> ProjectReport:
        raise NotImplementedError("The method update() is not implemented yet.")

    def delete_by_id(self, id_: ProjectReportId) -> None:
        raise NotImplementedError("The method delete_by_id() is not implemented yet.")
