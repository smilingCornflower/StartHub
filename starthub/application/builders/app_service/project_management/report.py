from application.builders.domain_service.project_management import ProjectReportServiceBuilder
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.project_management.report import ProjectReportAppService
from infrastructure.repositories.project.project import DjProjectReadRepository
from infrastructure.repositories.project.report import DjProjectReportReadRepository
from infrastructure.repositories.user_management.user import DjUserReadRepository


class ProjectReportAppServiceBuilder(AbstractAppServiceBuilder[ProjectReportAppService]):
    @staticmethod
    def create_service() -> ProjectReportAppService:
        return ProjectReportAppService(
            project_report_service=ProjectReportServiceBuilder.create_service(),
            report_read_repository=DjProjectReportReadRepository(),
            user_read_repository=DjUserReadRepository(),
            project_read_repository=DjProjectReadRepository(),
        )
