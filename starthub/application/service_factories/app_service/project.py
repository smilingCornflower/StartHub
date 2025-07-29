from application.ports.app_service_factory import AbstractAppServiceBuilder
from application.service_factories.domain_service.project_management import (
    CompanyFounderServiceBuilder,
    CompanyServiceBuilder,
    ProjectImageServiceBuilder,
    ProjectPhoneServiceBuilder,
    ProjectServiceBuilder,
    ProjectSocialLinkServiceBuilder,
    TeamMemberServiceBuilder,
)
from application.service_factories.domain_service.user_favorite import UserFavoriteServiceBuilder
from application.services.project import ProjectAppService
from infrastructure.cloud_storages.google import google_cloud_storage
from infrastructure.services.project_search import ProjectSearchService


class ProjectAppServiceBuilder(AbstractAppServiceBuilder[ProjectAppService]):
    @staticmethod
    def create_service() -> ProjectAppService:
        return ProjectAppService(
            project_service=ProjectServiceBuilder.create_service(),
            team_member_service=TeamMemberServiceBuilder.create_service(),
            project_phone_service=ProjectPhoneServiceBuilder.create_service(),
            project_social_link_service=ProjectSocialLinkServiceBuilder.create_service(),
            company_service=CompanyServiceBuilder.create_service(),
            company_founder_service=CompanyFounderServiceBuilder.create_service(),
            project_image_service=ProjectImageServiceBuilder.create_service(),
            google_cloud_storage=google_cloud_storage,
            user_favorite_service=UserFavoriteServiceBuilder.create_service(),
            project_search_service=ProjectSearchService(),
        )
