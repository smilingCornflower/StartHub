from application.builders.domain_service.project_management import ProjectAdminServiceBuilder
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.project_management.submission import ProjectAdminAppService
from infrastructure.repositories.project.project import DjProjectReadRepository
from infrastructure.repositories.user import DjUserReadRepository


class ProjectAdminAppServiceBuilder(AbstractAppServiceBuilder[ProjectAdminAppService]):
    @staticmethod
    def create_service() -> ProjectAdminAppService:
        return ProjectAdminAppService(
            project_admin_service=ProjectAdminServiceBuilder.create_service(),
            user_read_repository=DjUserReadRepository(),
            project_read_repository=DjProjectReadRepository(),
        )
