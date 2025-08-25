from application.dto.report import ProjectReportDto
from application.ports.service import AbstractAppService
from domain.models.project_management.report import ProjectReport
from domain.repositories.project.project import ProjectReadRepository
from domain.repositories.project.report import ProjectReportReadRepository
from domain.repositories.user_management.user import UserReadRepository
from domain.services.project_management.report import ProjectReportService
from domain.value_objects.common import Id, Pagination
from domain.value_objects.filter import ProjectReportFilter
from loguru import logger


class ProjectReportAppService(AbstractAppService):
    def __init__(
        self,
        project_report_service: ProjectReportService,
        report_read_repository: ProjectReportReadRepository,
        user_read_repository: UserReadRepository,
        project_read_repository: ProjectReadRepository,
    ):
        self._project_report_service = project_report_service
        self._report_read_repository = report_read_repository
        self._user_read_repository = user_read_repository
        self._project_read_repository = project_read_repository

    def get_reports_to_project(self, user_id: Id, project_id: Id, pagination: Pagination) -> list[ProjectReportDto]:
        user = self._user_read_repository.get_by_id(id_=user_id)
        project = self._project_read_repository.get_by_id(id_=project_id)
        self._project_report_service.check_can_user_read_reports_for_project(user=user, project=project)

        reports = self._report_read_repository.get_all(
            filter_=ProjectReportFilter(project_id=project_id), pagination=pagination
        )
        logger.debug(f"Found {len(reports)} reports")
        return [self._create_dto(i) for i in reports]

    def _create_dto(self, report: ProjectReport) -> ProjectReportDto:
        return ProjectReportDto(id=report.id, content=report.content, created_at=report.created_at)
