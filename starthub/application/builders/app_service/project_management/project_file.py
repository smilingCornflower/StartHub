from application.builders.domain_service.project_management import ProjectFileServiceBuilder
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.project_management.project_file import ProjectFileAppService
from infrastructure.repositories.project.project import DjProjectReadRepository
from infrastructure.repositories.project.project_file import DjProjectFileReadRepository
from infrastructure.repositories.user_management.user import DjUserReadRepository


class ProjectFileAppServiceBuilder(AbstractAppServiceBuilder[ProjectFileAppService]):
    @staticmethod
    def create_service() -> ProjectFileAppService:
        return ProjectFileAppService(
            project_file_service=ProjectFileServiceBuilder.create_service(),
            project_file_read_repository=DjProjectFileReadRepository(),
            user_read_repository=DjUserReadRepository(),
            project_read_repository=DjProjectReadRepository(),
        )
