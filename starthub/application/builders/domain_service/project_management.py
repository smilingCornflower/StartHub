from application.builders.domain_service.permission import PermissionServiceBuilder
from application.ports.domain_service_builder import AbstractDomainServiceBuilder
from domain.admin import ProjectAdmin
from domain.services.company import CompanyFounderService, CompanyService
from domain.services.project_management.accelerator import ProjectAcceleratorService
from domain.services.project_management.bank_loan import ProjectBankLoanService
from domain.services.project_management.bootsrtap import ProjectBootstrapService
from domain.services.project_management.crowdfunding import ProjectCrowdfundingService
from domain.services.project_management.government_grant import ProjectGovernmentGrantService
from domain.services.project_management.incubator import IncubatorService
from domain.services.project_management.investment import (
    ProjectInvestmentPhoneService,
    ProjectInvestmentService,
    ProjectInvestmentSocialLinkService,
)
from domain.services.project_management.media import ProjectMediaService
from domain.services.project_management.project import ProjectService
from domain.services.project_management.project_file import ProjectFileService
from domain.services.project_management.project_image import ProjectImageService
from domain.services.project_management.project_phone import ProjectPhoneService
from domain.services.project_management.project_social_link import ProjectSocialLinkService
from domain.services.project_management.step import ProjectStepService
from domain.services.project_management.submission import ProjectAdminService
from domain.services.project_management.team_member import TamMemberService
from domain.services.project_management.useful_link import ProjectUsefulLinkService
from infrastructure.cloud_storages.google import google_cloud_storage
from infrastructure.repositories.company import (
    DjCompanyFounderReadRepository,
    DjCompanyFounderWriteRepository,
    DjCompanyReadRepository,
    DjCompanyWriteRepository,
)
from infrastructure.repositories.geo.address import DjAddressWriteRepository
from infrastructure.repositories.geo.country import DjCountryReadRepository
from infrastructure.repositories.project.accelerator import DjProjectAcceleratorWriteRepository
from infrastructure.repositories.project.bank_loan import DjProjectBankLoanWriteRepository
from infrastructure.repositories.project.bootsrtap import DjProjectBootstrapWriteRepository
from infrastructure.repositories.project.crowdfunding import DjProjectCrowdfundingWriteRepository
from infrastructure.repositories.project.government_grant import DjProjectGovernmentGrantWriteRepository
from infrastructure.repositories.project.image import DjProjectImageReadRepository, DjProjectImageWriteRepository
from infrastructure.repositories.project.incubator import DjProjectIncubatorWriteRepository
from infrastructure.repositories.project.investment import (
    DjProjectInvestmentPhoneWriteRepository,
    DjProjectInvestmentReadRepository,
    DjProjectInvestmentSocialLinkWriteRepository,
    DjProjectInvestmentWriteRepository,
)
from infrastructure.repositories.project.media import DjProjectMediaReadRepository, DjProjectMediaWriteRepository
from infrastructure.repositories.project.phone import DjProjectPhoneReadRepository, DjProjectPhoneWriteRepository
from infrastructure.repositories.project.project import DjProjectReadRepository, DjProjectWriteRepository
from infrastructure.repositories.project.project_file import DjProjectFileWriteRepository
from infrastructure.repositories.project.social_link import (
    DjProjectSocialLinkReadRepository,
    DjProjectSocialLinkWriteRepository,
)
from infrastructure.repositories.project.step import DjProjectStepReadRepository, DjProjectStepWriteRepositroy
from infrastructure.repositories.project.team_member import DjTeamMemberReadRepository, DjTeamMemberWriteRepository
from infrastructure.repositories.project.useful_link import (
    DjProjectUsefulLinkReadRepository,
    DjProjectUsefulLinkWriteRepository,
)


class ProjectServiceBuilder(AbstractDomainServiceBuilder[ProjectService]):
    @staticmethod
    def create_service() -> ProjectService:
        return ProjectService(
            write_repository=DjProjectWriteRepository(), permission_service=PermissionServiceBuilder.create_service()
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
            address_write_repository=DjAddressWriteRepository(),
            permission_service=PermissionServiceBuilder.create_service(),
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


class ProjectStepServiceBuilder(AbstractDomainServiceBuilder[ProjectStepService]):
    @staticmethod
    def create_service() -> ProjectStepService:
        return ProjectStepService(
            read_repository=DjProjectStepReadRepository(),
            write_repository=DjProjectStepWriteRepositroy(),
        )


class ProjectIncubatorServiceBuilder(AbstractDomainServiceBuilder[IncubatorService]):
    @staticmethod
    def create_service() -> IncubatorService:
        return IncubatorService(
            write_repository=DjProjectIncubatorWriteRepository(),
            permission_service=PermissionServiceBuilder.create_service(),
        )


class ProjectAcceleratorServiceBuilder(AbstractDomainServiceBuilder[ProjectAcceleratorService]):
    @staticmethod
    def create_service() -> ProjectAcceleratorService:
        return ProjectAcceleratorService(
            write_repository=DjProjectAcceleratorWriteRepository(),
            permission_service=PermissionServiceBuilder.create_service(),
        )


class ProjectCrowdfundingServiceBuilder(AbstractDomainServiceBuilder[ProjectCrowdfundingService]):
    @staticmethod
    def create_service() -> ProjectCrowdfundingService:
        return ProjectCrowdfundingService(
            write_repository=DjProjectCrowdfundingWriteRepository(),
            permission_service=PermissionServiceBuilder.create_service(),
        )


class ProjectInvestmentServiceBuilder(AbstractDomainServiceBuilder[ProjectInvestmentService]):
    @staticmethod
    def create_service() -> ProjectInvestmentService:
        return ProjectInvestmentService(
            write_repository=DjProjectInvestmentWriteRepository(),
            permission_service=PermissionServiceBuilder.create_service(),
            project_investment_read_repository=DjProjectInvestmentReadRepository(),
        )


class ProjectInvestmentSocialLinkServiceBuilder(AbstractDomainServiceBuilder[ProjectInvestmentSocialLinkService]):
    @staticmethod
    def create_service() -> ProjectInvestmentSocialLinkService:
        return ProjectInvestmentSocialLinkService(
            write_repository=DjProjectInvestmentSocialLinkWriteRepository(),
            permission_service=PermissionServiceBuilder.create_service(),
        )


class ProjectInvestmentPhoneServiceBuilder(AbstractDomainServiceBuilder[ProjectInvestmentPhoneService]):
    @staticmethod
    def create_service() -> ProjectInvestmentPhoneService:
        return ProjectInvestmentPhoneService(
            write_repository=DjProjectInvestmentPhoneWriteRepository(),
            permission_service=PermissionServiceBuilder.create_service(),
        )


class ProjectGovernmentGrantServiceBuilder(AbstractDomainServiceBuilder[ProjectGovernmentGrantService]):
    @staticmethod
    def create_service() -> ProjectGovernmentGrantService:
        return ProjectGovernmentGrantService(
            write_repository=DjProjectGovernmentGrantWriteRepository(),
            permission_service=PermissionServiceBuilder.create_service(),
        )


class ProjectBootstrapServiceBuilder(AbstractDomainServiceBuilder[ProjectBootstrapService]):
    @staticmethod
    def create_service() -> ProjectBootstrapService:
        return ProjectBootstrapService(
            write_repository=DjProjectBootstrapWriteRepository(),
            permission_service=PermissionServiceBuilder.create_service(),
        )


class ProjectBankLoanServiceBuilder(AbstractDomainServiceBuilder[ProjectBankLoanService]):
    @staticmethod
    def create_service() -> ProjectBankLoanService:
        return ProjectBankLoanService(
            write_repository=DjProjectBankLoanWriteRepository(),
            permission_service=PermissionServiceBuilder.create_service(),
        )


class ProjectFileServiceBuilder(AbstractDomainServiceBuilder[ProjectFileService]):
    @staticmethod
    def create_service() -> ProjectFileService:
        return ProjectFileService(
            permission_service=PermissionServiceBuilder.create_service(),
            cloud_storage=google_cloud_storage,
            write_repository=DjProjectFileWriteRepository(),
        )


class ProjectMediaServiceBuilder(AbstractDomainServiceBuilder[ProjectMediaService]):
    @staticmethod
    def create_service() -> ProjectMediaService:
        return ProjectMediaService(
            write_repository=DjProjectMediaWriteRepository(),
            read_repository=DjProjectMediaReadRepository(),
            permission_service=PermissionServiceBuilder.create_service(),
            clous_storage=google_cloud_storage,
        )


class ProjectUsefulLinkServiceBuilder(AbstractDomainServiceBuilder[ProjectUsefulLinkService]):
    @staticmethod
    def create_service() -> ProjectUsefulLinkService:
        return ProjectUsefulLinkService(
            permission_service=PermissionServiceBuilder.create_service(),
            write_repository=DjProjectUsefulLinkWriteRepository(),
            read_repository=DjProjectUsefulLinkReadRepository(),
        )


class ProjectAdminServiceBuilder(AbstractDomainServiceBuilder[ProjectAdminService]):
    @staticmethod
    def create_service() -> ProjectAdminService:
        return ProjectAdminService(
            permisison_service=PermissionServiceBuilder.create_service(),
            project_write_repository=DjProjectWriteRepository(),
        )
