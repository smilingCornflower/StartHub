from application.builders.domain_service.project_management import ProjectCrowdfundingServiceBuilder
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.project_management.crowdfunding import CrowdfundingAppService
from infrastructure.repositories.project.crowdfunding import DjProjectCrowdFundingReadRepository
from infrastructure.repositories.project.project import DjProjectReadRepository
from infrastructure.repositories.user_management.user import DjUserReadRepository


class CrowdfundingAppServiceBuilder(AbstractAppServiceBuilder[CrowdfundingAppService]):
    @staticmethod
    def create_service() -> CrowdfundingAppService:
        return CrowdfundingAppService(
            crowdfunding_service=ProjectCrowdfundingServiceBuilder.create_service(),
            read_repository=DjProjectCrowdFundingReadRepository(),
            user_read_repository=DjUserReadRepository(),
            project_read_repository=DjProjectReadRepository(),
        )
