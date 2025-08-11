from application.builders.domain_service.project_management import ProjectInvestmentServiceBuilder
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.project_management.investment import ProjectInvestmentAppService
from infrastructure.repositories.project.project import DjProjectReadRepository
from infrastructure.repositories.user import DjUserReadRepository


class ProjectInvestmentAppServiceBuilder(AbstractAppServiceBuilder[ProjectInvestmentAppService]):
    @staticmethod
    def create_service() -> ProjectInvestmentAppService:
        return ProjectInvestmentAppService(
            project_investment_service=ProjectInvestmentServiceBuilder.create_service(),
            user_read_repository=DjUserReadRepository(),
            project_read_repository=DjProjectReadRepository(),
        )
