from application.builders.domain_service.project_management import ProjectResubmitServiceBuilder
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.project_management.resubmit import ProjectResubmitAppService
from infrastructure.repositories.project.project import DjProjectReadRepository
from infrastructure.repositories.user_management.user import DjUserReadRepository


class ProjectResubmitAppServiceBuilder(AbstractAppServiceBuilder[ProjectResubmitAppService]):
    @staticmethod
    def create_service() -> ProjectResubmitAppService:
        return ProjectResubmitAppService(
            project_resubmit_service=ProjectResubmitServiceBuilder.create_service(),
            user_read_repository=DjUserReadRepository(),
            project_read_repository=DjProjectReadRepository(),
        )
