from domain.models.project_management.report import ProjectReport
from domain.repositories.project.report import ProjectReportReadRepository, ProjectReportWriteRepository
from domain.value_objects.common import CursorPagination, OffsetPagination
from domain.value_objects.filter import ProjectReportFilter
from domain.value_objects.project.report import ProjectReportCreatePayload, ProjectReportId, ProjectUpdatePayload
from infrastructure.repositories.pagination import apply_pagination


class DjProjectReportReadRepository(ProjectReportReadRepository):
    def get_by_id(self, id_: ProjectReportId) -> ProjectReport:
        raise NotImplementedError("The method get_by_id() is not implemented yet.")

    def get_all(
        self, filter_: ProjectReportFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[ProjectReport]:
        queryset = ProjectReport.objects.all()

        if filter_.project_id is not None:
            queryset = queryset.filter(project_id=filter_.project_id.value)

        if pagination:
            return apply_pagination(queryset, pagination=pagination)

        return list(queryset)


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
