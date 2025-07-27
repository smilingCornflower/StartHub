from application.ports.domain_service_factory import AbstractDomainServiceBuilder
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


class ProjectServiceBuilder(AbstractDomainServiceBuilder[ProjectService]):
    @staticmethod
    def create_service() -> ProjectService:
        return ProjectService(
            project_read_repository=DjProjectReadRepository(),
            project_write_repository=DjProjectWriteRepository(),
            project_category_read_repository=DjProjectCategoryReadRepository(),
            funding_model_read_repository=DjFundingModelReadRepository(),
            user_read_repository=DjUserReadRepository(),
            company_read_repository=DjCompanyReadRepository(),
            company_write_repository=DjCompanyWriteRepository(),
            cloud_storage=google_cloud_storage,
            pdf_service=PdfService(),
        )


class TeamMemberServiceBuilder(AbstractDomainServiceBuilder[TamMemberService]):
    @staticmethod
    def create_service() -> TamMemberService:
        return TamMemberService(
            team_member_read_repository=DjTeamMemberReadRepository(),
            team_member_write_repository=DjTeamMemberWriteRepository(),
        )


class ProjectPhoneServiceBuilder(AbstractDomainServiceBuilder[ProjectPhoneService]):
    @staticmethod
    def create_service() -> ProjectPhoneService:
        return ProjectPhoneService(
            project_phone_read_repository=DjProjectPhoneReadRepository(),
            project_phone_write_repository=DjProjectPhoneWriteRepository(),
        )


class ProjectSocialLinkServiceBuilder(AbstractDomainServiceBuilder[ProjectSocialLinkService]):
    @staticmethod
    def create_service() -> ProjectSocialLinkService:
        return ProjectSocialLinkService(
            read_repository=DjProjectSocialLinkReadRepository(),
            write_repository=DjProjectSocialLinkWriteRepository(),
        )


class CompanyServiceBuilder(AbstractDomainServiceBuilder[CompanyService]):
    @staticmethod
    def create_service() -> CompanyService:
        return CompanyService(
            company_write_repository=DjCompanyWriteRepository(),
            country_read_repository=DjCountryReadRepository(),
            company_read_repository=DjCompanyReadRepository(),
        )


class CompanyFounderServiceBuilder(AbstractDomainServiceBuilder[CompanyFounderService]):
    @staticmethod
    def create_service() -> CompanyFounderService:
        return CompanyFounderService(
            company_founder_read_repository=DjCompanyFounderReadRepository(),
            company_founder_write_repository=DjCompanyFounderWriteRepository(),
        )


class ProjectImageServiceBuilder(AbstractDomainServiceBuilder[ProjectImageService]):
    @staticmethod
    def create_service() -> ProjectImageService:
        return ProjectImageService(
            project_image_read_repository=DjProjectImageReadRepository(),
            project_image_write_repository=DjProjectImageWriteRepository(),
            project_read_repository=DjProjectReadRepository(),
            cloud_storage=google_cloud_storage,
        )
