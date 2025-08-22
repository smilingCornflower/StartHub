from application.builders.domain_service.project_management import (
    ProjectAcceleratorServiceBuilder,
    ProjectIncubatorServiceBuilder,
    ProjectServiceBuilder,
    ProjectStepServiceBuilder,
)
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.project_management.project import (
    ProjectCreateAppService,
    ProjectDeleteAppService,
    ProjectGetAppService,
    ProjectUpdateAppService,
)
from infrastructure.cloud_storages.google import google_cloud_storage
from infrastructure.repositories.company import DjCompanyReadRepository
from infrastructure.repositories.geo.city import DjCityReadRepository
from infrastructure.repositories.geo.country import DjCountryReadRepository
from infrastructure.repositories.geo.region import DjRegionReadRepository
from infrastructure.repositories.project.accelerator import DjProjectAcceleratorReadRepository
from infrastructure.repositories.project.bank_loan import DjProjectBankLoanReadRepository
from infrastructure.repositories.project.bootsrtap import DjProjectBootstrapReadRepository
from infrastructure.repositories.project.category import DjProjectCategoryReadRepository
from infrastructure.repositories.project.crowdfunding import DjProjectCrowdFundingReadRepository
from infrastructure.repositories.project.funding_model import DjFundingModelReadRepository
from infrastructure.repositories.project.government_grant import DjProjectGovernmentGrantReadRepository
from infrastructure.repositories.project.image import DjProjectImageReadRepository
from infrastructure.repositories.project.incubator import DjProjectIncubatorReadRepository
from infrastructure.repositories.project.investment import (
    DjProjectInvestmentPhoneReadRepository,
    DjProjectInvestmentReadRepository,
    DjProjectInvestmentSocialLinkReadRepository,
)
from infrastructure.repositories.project.media import DjProjectMediaReadRepository
from infrastructure.repositories.project.project import DjProjectReadRepository
from infrastructure.repositories.project.project_file import DjProjectFileReadRepository
from infrastructure.repositories.project.step import DjProjectStepReadRepository
from infrastructure.repositories.project.useful_link import DjProjectUsefulLinkReadRepository
from infrastructure.repositories.user import DjUserReadRepository
from infrastructure.repositories.user_favorite import DjUserFavoriteReadRepository
from infrastructure.services.project_search import ProjectSearchService


class ProjectCreateAppServiceBuilder(AbstractAppServiceBuilder[ProjectCreateAppService]):
    @staticmethod
    def create_service() -> ProjectCreateAppService:
        return ProjectCreateAppService(
            project_service=ProjectServiceBuilder.create_service(),
            project_step_service=ProjectStepServiceBuilder.create_service(),
            cloud_storage=google_cloud_storage,
            user_read_repository=DjUserReadRepository(),
            funding_model_read_repository=DjFundingModelReadRepository(),
            company_read_repository=DjCompanyReadRepository(),
            country_read_repository=DjCountryReadRepository(),
            project_category_read_repository=DjProjectCategoryReadRepository(),
            city_read_repository=DjCityReadRepository(),
            region_read_repository=DjRegionReadRepository(),
        )


class ProjectUpdateAppServiceBuilder(AbstractAppServiceBuilder[ProjectUpdateAppService]):
    @staticmethod
    def create_service() -> ProjectUpdateAppService:

        return ProjectUpdateAppService(
            project_service=ProjectServiceBuilder.create_service(),
            project_step_service=ProjectStepServiceBuilder.create_service(),
            incubator_service=ProjectIncubatorServiceBuilder.create_service(),
            accelerator_service=ProjectAcceleratorServiceBuilder.create_service(),
            incubator_read_repository=DjProjectIncubatorReadRepository(),
            accelerator_read_repository=DjProjectAcceleratorReadRepository(),
            user_read_repository=DjUserReadRepository(),
            project_read_repository=DjProjectReadRepository(),
            project_category_read_repository=DjProjectCategoryReadRepository(),
            funding_model_read_repository=DjFundingModelReadRepository(),
            cloud_storage=google_cloud_storage,
        )


class ProjectGetAppServiceBuilder(AbstractAppServiceBuilder[ProjectGetAppService]):
    @staticmethod
    def create_service() -> ProjectGetAppService:
        return ProjectGetAppService(
            project_read_repository=DjProjectReadRepository(),
            project_media_read_repository=DjProjectMediaReadRepository(),
            project_file_read_repository=DjProjectFileReadRepository(),
            project_category_read_repository=DjProjectCategoryReadRepository(),
            user_favorite_read_repository=DjUserFavoriteReadRepository(),
            project_step_read_repository=DjProjectStepReadRepository(),
            project_search_service=ProjectSearchService(),
            project_accelerator_read_repository=DjProjectAcceleratorReadRepository(),
            project_incubator_read_repository=DjProjectIncubatorReadRepository(),
            project_crowdfunding_read_repository=DjProjectCrowdFundingReadRepository(),
            project_investment_read_repository=DjProjectInvestmentReadRepository(),
            project_investment_social_link_read_repository=DjProjectInvestmentSocialLinkReadRepository(),
            project_investment_phone_read_repository=DjProjectInvestmentPhoneReadRepository(),
            project_government_grant_read_repository=DjProjectGovernmentGrantReadRepository(),
            project_bank_loan_read_repository=DjProjectBankLoanReadRepository(),
            project_bootstrap_read_repository=DjProjectBootstrapReadRepository(),
            project_useful_link_read_repository=DjProjectUsefulLinkReadRepository(),
            cloud_storage=google_cloud_storage,
        )


class ProjectDeleteAppServiceBuilder(AbstractAppServiceBuilder[ProjectDeleteAppService]):
    @staticmethod
    def create_service() -> ProjectDeleteAppService:
        return ProjectDeleteAppService(
            project_service=ProjectServiceBuilder.create_service(),
            user_read_repository=DjUserReadRepository(),
            project_read_repository=DjProjectReadRepository(),
            project_image_read_repository=DjProjectImageReadRepository(),
        )
