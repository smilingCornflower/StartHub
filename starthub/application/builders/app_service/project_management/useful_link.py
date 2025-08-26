from application.builders.domain_service.project_management import ProjectUsefulLinkServiceBuilder
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.project_management.useful_link import ProjectUsefulLinkAppService
from infrastructure.repositories.project.project import DjProjectReadRepository
from infrastructure.repositories.project.useful_link import DjProjectUsefulLinkReadRepository
from infrastructure.repositories.user_management.user import DjUserReadRepository


class ProjectUsefulLinkAppServiceBuilder(AbstractAppServiceBuilder[ProjectUsefulLinkAppService]):
    @staticmethod
    def create_service() -> ProjectUsefulLinkAppService:
        return ProjectUsefulLinkAppService(
            service=ProjectUsefulLinkServiceBuilder.create_service(),
            useful_link_read_repository=DjProjectUsefulLinkReadRepository(),
            user_read_repository=DjUserReadRepository(),
            project_read_repository=DjProjectReadRepository(),
        )
