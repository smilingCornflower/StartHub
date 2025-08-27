from application.builders.domain_service.project_management import FundingModelServiceBuilder
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.project_management.funding_model import FundingModelAppService
from infrastructure.repositories.project.funding_model import DjFundingModelReadRepository
from infrastructure.repositories.user_management.user import DjUserReadRepository


class FundingModelAppServiceBuilder(AbstractAppServiceBuilder[FundingModelAppService]):
    @staticmethod
    def create_service() -> FundingModelAppService:
        return FundingModelAppService(
            funding_model_service=FundingModelServiceBuilder.create_service(),
            user_read_repository=DjUserReadRepository(),
            funding_model_read_repository=DjFundingModelReadRepository(),
        )
