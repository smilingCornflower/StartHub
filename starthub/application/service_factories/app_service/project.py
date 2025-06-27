from application.ports.app_service_factory import AbstractAppServiceFactory
from application.service_factories.domain_service.project_management import (
    CompanyFounderServiceFactory,
    CompanyServiceFactory,
    ProjectImageServiceFactory,
    ProjectPhoneServiceFactory,
    ProjectServiceFactory,
    ProjectSocialLinkServiceFactory,
    TeamMemberServiceFactory,
)
from application.services.project import ProjectAppService
from infrastructure.cloud_storages.google import google_cloud_storage


class ProjectAppServiceFactory(AbstractAppServiceFactory[ProjectAppService]):
    @staticmethod
    def create_service() -> ProjectAppService:
        return ProjectAppService(
            project_service=ProjectServiceFactory.create_service(),
            team_member_service=TeamMemberServiceFactory.create_service(),
            project_phone_service=ProjectPhoneServiceFactory.create_service(),
            project_social_link_service=ProjectSocialLinkServiceFactory.create_service(),
            company_service=CompanyServiceFactory.create_service(),
            company_founder_service=CompanyFounderServiceFactory.create_service(),
            project_image_service=ProjectImageServiceFactory.create_service(),
            google_cloud_storage=google_cloud_storage,
        )
