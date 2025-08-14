from application.builders.domain_service.project_management import ProjectFileServiceBuilder
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.project_management.project_file import ProjectFileAppService
from infrastructure.repositories.project.project import DjProjectReadRepository
from infrastructure.repositories.user import DjUserReadRepository


class ProjectFileAppServiceBuilder(AbstractAppServiceBuilder[ProjectFileAppService]):
    @staticmethod
    def create_service() -> ProjectFileAppService:
        return ProjectFileAppService(
            project_file_service=ProjectFileServiceBuilder.create_service(),
            user_read_repository=DjUserReadRepository(),
            project_read_repository=DjProjectReadRepository(),
        )
