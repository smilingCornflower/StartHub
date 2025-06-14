from application.ports.service_factory import AbstractAppServiceFactory
from application.services.project import ProjectAppService
from domain.services.company import CompanyFounderService, CompanyService
from domain.services.file import PdfService
from domain.services.project_management import (
    ProjectImageService,
    ProjectPhoneService,
    ProjectService,
    ProjectSocialLinkService,
    TamMemberService,
)
from infrastructure.cloud_storages.google import google_cloud_storage
from infrastructure.repositories.company import (
    DjCompanyFounderReadRepository,
    DjCompanyFounderWriteRepository,
    DjCompanyReadRepository,
    DjCompanyWriteRepository,
)
from infrastructure.repositories.country import DjCountryReadRepository
from infrastructure.repositories.project_management import (
    DjFundingModelReadRepository,
    DjProjectCategoryReadRepository,
    DjProjectImageReadRepository,
    DjProjectImageWriteRepository,
    DjProjectPhoneReadRepository,
    DjProjectPhoneWriteRepository,
    DjProjectReadRepository,
    DjProjectSocialLinkReadRepository,
    DjProjectSocialLinkWriteRepository,
    DjProjectWriteRepository,
    DjTeamMemberReadRepository,
    DjTeamMemberWriteRepository,
)
from infrastructure.repositories.user import DjUserReadRepository


class ProjectAppServiceFactory(AbstractAppServiceFactory[ProjectAppService]):
    @staticmethod
    def create_service() -> ProjectAppService:
        return ProjectAppService(
            project_service=ProjectService(
                project_read_repository=DjProjectReadRepository(),
                project_write_repository=DjProjectWriteRepository(),
                project_category_read_repository=DjProjectCategoryReadRepository(),
                funding_model_read_repository=DjFundingModelReadRepository(),
                user_read_repository=DjUserReadRepository(),
                company_read_repository=DjCompanyReadRepository(),
                company_write_repository=DjCompanyWriteRepository(),
                cloud_storage=google_cloud_storage,
                pdf_service=PdfService(),
            ),
            team_member_service=TamMemberService(
                team_member_read_repository=DjTeamMemberReadRepository(),
                team_member_write_repository=DjTeamMemberWriteRepository(),
            ),
            project_phone_service=ProjectPhoneService(
                project_phone_read_repository=DjProjectPhoneReadRepository(),
                project_phone_write_repository=DjProjectPhoneWriteRepository(),
            ),
            project_social_link_service=ProjectSocialLinkService(
                read_repository=DjProjectSocialLinkReadRepository(),
                write_repository=DjProjectSocialLinkWriteRepository(),
            ),
            company_service=CompanyService(
                company_write_repository=DjCompanyWriteRepository(),
                country_read_repository=DjCountryReadRepository(),
                company_read_repository=DjCompanyReadRepository(),
            ),
            company_founder_service=CompanyFounderService(
                company_founder_read_repository=DjCompanyFounderReadRepository(),
                company_founder_write_repository=DjCompanyFounderWriteRepository(),
            ),
            project_image_service=ProjectImageService(
                project_image_read_repository=DjProjectImageReadRepository(),
                project_image_write_repository=DjProjectImageWriteRepository(),
                project_read_repository=DjProjectReadRepository(),
                cloud_storage=google_cloud_storage,
            ),
        )


project_app_service: ProjectAppService = ProjectAppServiceFactory.create_service()
