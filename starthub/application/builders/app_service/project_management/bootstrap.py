from application.builders.domain_service.project_management import ProjectBootstrapServiceBuilder
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.project_management.bootsrtap import ProjectBootstrapAppService
from infrastructure.repositories.project.bootsrtap import DjProjectBootstrapReadRepository
from infrastructure.repositories.project.project import DjProjectReadRepository
from infrastructure.repositories.user import DjUserReadRepository


class ProjectBootstrapAppServiceBuilder(AbstractAppServiceBuilder[ProjectBootstrapAppService]):
    @staticmethod
    def create_service() -> ProjectBootstrapAppService:
        return ProjectBootstrapAppService(
            bootstrap_service=ProjectBootstrapServiceBuilder.create_service(),
            bootstrap_read_repository=DjProjectBootstrapReadRepository(),
            user_read_repository=DjUserReadRepository(),
            project_read_repository=DjProjectReadRepository(),
        )
