from application.builders.domain_service.project_management import ProjectGovernmentGrantServiceBuilder
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.project_management.government_grant import GovernmentGrantAppService
from infrastructure.repositories.project.government_grant import DjProjectGovernmentGrantReadRepository
from infrastructure.repositories.project.project import DjProjectReadRepository
from infrastructure.repositories.user_management.user import DjUserReadRepository


class GovernmentGrantAppServiceBuilder(AbstractAppServiceBuilder[GovernmentGrantAppService]):
    @staticmethod
    def create_service() -> GovernmentGrantAppService:
        return GovernmentGrantAppService(
            government_grant_service=ProjectGovernmentGrantServiceBuilder.create_service(),
            user_read_repository=DjUserReadRepository(),
            project_read_repository=DjProjectReadRepository(),
            government_grant_read_repository=DjProjectGovernmentGrantReadRepository(),
        )
