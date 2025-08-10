from application.ports.app_service_builder import AbstractAppServiceBuilder, S
from application.services.project_management.crowdfunding import CrowdfundingAppService
from infrastructure.repositories.project.crowdfunding import DjProjectCrowdFundingReadRepository
from application.builders.domain_service.project_management import ProjectCrowdfundingServiceBuilder
from infrastructure.repositories.user import DjUserReadRepository


class CrowdfundingAppServiceBuilder(AbstractAppServiceBuilder[CrowdfundingAppService]):
    @staticmethod
    def create_service() -> CrowdfundingAppService:
        return CrowdfundingAppService(
            crowdfunding_service=ProjectCrowdfundingServiceBuilder.create_service(),
            read_repository=DjProjectCrowdFundingReadRepository(),
            user_read_repository=DjUserReadRepository(),
        )