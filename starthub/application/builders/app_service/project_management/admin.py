from application.builders.app_service.project_management.project import ProjectGetAppServiceBuilder
from application.builders.domain_service.project_management import ProjectAdminServiceBuilder
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.project_management.admin import ProjectAdminAppService
from infrastructure.repositories.project.project import DjProjectReadRepository
from infrastructure.repositories.user_management.user import DjUserReadRepository


class ProjectAdminAppServiceBuilder(AbstractAppServiceBuilder[ProjectAdminAppService]):
    @staticmethod
    def create_service() -> ProjectAdminAppService:
        return ProjectAdminAppService(
            project_admin_service=ProjectAdminServiceBuilder.create_service(),
            user_read_repository=DjUserReadRepository(),
            project_read_repository=DjProjectReadRepository(),
            project_get_app_service=ProjectGetAppServiceBuilder.create_service(),
        )
