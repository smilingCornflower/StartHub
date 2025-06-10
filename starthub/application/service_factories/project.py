from application.ports.service_factory import AbstractServiceFactory
from application.services.project import ProjectAppService
from domain.services.company import CompanyService
from domain.services.file import PdfService
from domain.services.project_management import (
    ProjectPhoneService,
    ProjectService,
    ProjectSocialLinkService,
    TamMemberService,
)
from infrastructure.cloud_storages.google import google_cloud_storage
from infrastructure.repositories.company import DjCompanyReadRepository, DjCompanyWriteRepository, \
    DjCompanyFounderWriteRepository
from infrastructure.repositories.country import DjCountryReadRepository
from infrastructure.repositories.project_management import (
    DjFundingModelReadRepository,
    DjProjectCategoryReadRepository,
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


class ProjectServiceFactory(AbstractServiceFactory[ProjectAppService]):
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
                user_read_repository=DjUserReadRepository(),
                country_read_repository=DjCountryReadRepository(),
                founder_write_repository=DjCompanyFounderWriteRepository(),
                company_read_repository=DjCompanyReadRepository(),
            )
        )


project_app_service: ProjectAppService = ProjectServiceFactory.create_service()
