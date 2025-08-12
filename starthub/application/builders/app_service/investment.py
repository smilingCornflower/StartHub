from application.builders.domain_service.project_management import (
    ProjectInvestmentPhoneServiceBuilder,
    ProjectInvestmentServiceBuilder,
    ProjectInvestmentSocialLinkServiceBuilder,
)
from application.ports.app_service_builder import AbstractAppServiceBuilder
from application.services.project_management.investment import ProjectInvestmentAppService
from application.services.project_management.project_investment_phone import ProjectInvestmentPhoneAppService
from application.services.project_management.project_investment_social_link import ProjectInvestmentSocialLinkAppService
from infrastructure.repositories.project.investment import (
    DjProjectInvestmentPhoneReadRepository,
    DjProjectInvestmentReadRepository,
    DjProjectInvestmentSocialLinkReadRepository,
)
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


class ProjectInvestmentSocialLinkAppServiceBuilder(AbstractAppServiceBuilder[ProjectInvestmentSocialLinkAppService]):
    @staticmethod
    def create_service() -> ProjectInvestmentSocialLinkAppService:
        return ProjectInvestmentSocialLinkAppService(
            user_read_repository=DjUserReadRepository(),
            project_read_repository=DjProjectReadRepository(),
            project_investment_social_link_service=ProjectInvestmentSocialLinkServiceBuilder.create_service(),
            project_investment_social_link_read_repository=DjProjectInvestmentSocialLinkReadRepository(),
            project_investment_read_repository=DjProjectInvestmentReadRepository(),
        )


class ProjectInvestmentPhoneAppServiceBuilder(AbstractAppServiceBuilder[ProjectInvestmentPhoneAppService]):
    @staticmethod
    def create_service() -> ProjectInvestmentPhoneAppService:
        return ProjectInvestmentPhoneAppService(
            project_investment_phone_service=ProjectInvestmentPhoneServiceBuilder.create_service(),
            investment_read_repository=DjProjectInvestmentReadRepository(),
            project_read_repository=DjProjectReadRepository(),
            user_read_repository=DjUserReadRepository(),
            project_investment_phone_read_repository=DjProjectInvestmentPhoneReadRepository(),
        )
