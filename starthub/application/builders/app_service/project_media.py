from application.builders.domain_service.project_management import ProjectMediaServiceBuilder
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.project_management.project_media import ProjectMediaAppService
from infrastructure.repositories.project.media import DjProjectMediaReadRepository
from infrastructure.repositories.project.project import DjProjectReadRepository
from infrastructure.repositories.user import DjUserReadRepository


class ProjectMediaAppServiceBuilder(AbstractAppServiceBuilder[ProjectMediaAppService]):
    @staticmethod
    def create_service() -> ProjectMediaAppService:
        return ProjectMediaAppService(
            project_media_service=ProjectMediaServiceBuilder.create_service(),
            project_media_read_repository=DjProjectMediaReadRepository(),
            user_read_repository=DjUserReadRepository(),
            project_read_repository=DjProjectReadRepository(),
        )
