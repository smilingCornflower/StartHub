from application.builders.app_service.auth import AuthAppServiceBuilder, RegistrationAppServiceBuilder
from application.builders.app_service.company import CompanyAppServiceBuilder
from application.builders.app_service.geo import CityAppServiceBuilder, RegionAppServiceBuilder
from application.builders.app_service.news import NewsAppServiceBuilder
from application.builders.app_service.notification import NotificationAppServiceBuilder
from application.builders.app_service.project_management.accelerator import AcceleratorAppServiceBuilder
from application.builders.app_service.project_management.admin import ProjectAdminAppServiceBuilder
from application.builders.app_service.project_management.bank_loan import ProjectBankLoanAppServiceBuilder
from application.builders.app_service.project_management.bootstrap import ProjectBootstrapAppServiceBuilder
from application.builders.app_service.project_management.crowdfunding import CrowdfundingAppServiceBuilder
from application.builders.app_service.project_management.government_grant import GovernmentGrantAppServiceBuilder
from application.builders.app_service.project_management.investment import (
    ProjectInvestmentAppServiceBuilder,
    ProjectInvestmentPhoneAppServiceBuilder,
    ProjectInvestmentSocialLinkAppServiceBuilder,
)
from application.builders.app_service.project_management.project import (
    ProjectCreateAppServiceBuilder,
    ProjectDeleteAppServiceBuilder,
    ProjectGetAppServiceBuilder,
    ProjectUpdateAppServiceBuilder,
)
from application.builders.app_service.project_management.project_file import ProjectFileAppServiceBuilder
from application.builders.app_service.project_management.project_image import ProjectImageAppServiceBuilder
from application.builders.app_service.project_management.project_media import ProjectMediaAppServiceBuilder
from application.builders.app_service.project_management.useful_link import ProjectUsefulLinkAppServiceBuilder
from application.builders.app_service.user import UserAdminAppServiceBuilder, UserAppServiceBuilder
from application.builders.app_service.user_favorite import UserFavoriteAppAppServiceBuilder
from application.services.auth import AuthAppService, RegistrationAppService
from application.services.company import CompanyAppService
from application.services.geo.city import CityAppService
from application.services.geo.region import RegionAppService
from application.services.news import NewsAppService
from application.services.notification import NotificationAppService
from application.services.project_management.accelerator import AcceleratorAppService
from application.services.project_management.admin import ProjectAdminAppService
from application.services.project_management.bank_loan import ProjectBankLoanAppService
from application.services.project_management.bootsrtap import ProjectBootstrapAppService
from application.services.project_management.crowdfunding import CrowdfundingAppService
from application.services.project_management.government_grant import GovernmentGrantAppService
from application.services.project_management.investment import ProjectInvestmentAppService
from application.services.project_management.project import (
    ProjectCreateAppService,
    ProjectDeleteAppService,
    ProjectGetAppService,
    ProjectUpdateAppService,
)
from application.services.project_management.project_file import ProjectFileAppService
from application.services.project_management.project_image import ProjectImageAppService
from application.services.project_management.project_investment_phone import ProjectInvestmentPhoneAppService
from application.services.project_management.project_investment_social_link import ProjectInvestmentSocialLinkAppService
from application.services.project_management.project_media import ProjectMediaAppService
from application.services.project_management.useful_link import ProjectUsefulLinkAppService
from application.services.user_management.admin import UserAdminAppService
from application.services.user_management.user import UserAppService
from application.services.user_management.user_favorite import UserFavoriteAppService
from infrastructure.services.cookie import CookieService, cookie_service


class Gateway:
    _auth_app_service: AuthAppService | None = None
    _registration_app_service: RegistrationAppService | None = None

    _user_app_service: UserAppService | None = None

    _project_create_app_service: ProjectCreateAppService | None = None
    _project_update_app_service: ProjectUpdateAppService | None = None
    _project_get_app_service: ProjectGetAppService | None = None
    _project_delete_app_service: ProjectDeleteAppService | None = None

    _project_image_app_service: ProjectImageAppService | None = None
    _user_favorite_app_service: UserFavoriteAppService | None = None
    _news_app_service: NewsAppService | None = None
    _company_app_service: CompanyAppService | None = None
    _accelerator_app_service: AcceleratorAppService | None = None
    _crowdfunding_app_service: CrowdfundingAppService | None = None
    _project_investment_app_service: ProjectInvestmentAppService | None = None
    _project_investment_social_link_app_service: ProjectInvestmentSocialLinkAppService | None = None
    _project_investment_phone_app_service: ProjectInvestmentPhoneAppService | None = None
    _proejct_government_grant_app_service: GovernmentGrantAppService | None = None
    _project_bootstrap_app_service: ProjectBootstrapAppService | None = None
    _project_bank_load_app_service: ProjectBankLoanAppService | None = None
    _project_file_app_service: ProjectFileAppService | None = None
    _project_media_app_service: ProjectMediaAppService | None = None
    _project_useful_link_app_service: ProjectUsefulLinkAppService | None = None
    _project_admin_app_service: ProjectAdminAppService | None = None
    _user_admin_app_service: UserAdminAppService | None = None

    _region_app_service: RegionAppService | None = None
    _city_app_service: CityAppService | None = None

    _notification_app_service: NotificationAppService | None = None
    _cookie_service: CookieService | None = None

    @property
    def auth_app_service(self) -> AuthAppService:
        if self._auth_app_service is None:
            self._auth_app_service = AuthAppServiceBuilder.create_service()
        return self._auth_app_service

    @property
    def registration_app_service(self) -> RegistrationAppService:
        if self._registration_app_service is None:
            self._registration_app_service = RegistrationAppServiceBuilder.create_service()
        return self._registration_app_service

    @property
    def user_app_service(self) -> UserAppService:
        if self._user_app_service is None:
            self._user_app_service = UserAppServiceBuilder.create_service()
        return self._user_app_service

    @property
    def project_create_app_service(self) -> ProjectCreateAppService:
        if self._project_create_app_service is None:
            self._project_create_app_service = ProjectCreateAppServiceBuilder.create_service()
        return self._project_create_app_service

    @property
    def project_update_app_service(self) -> ProjectUpdateAppService:
        if self._project_update_app_service is None:
            self._project_update_app_service = ProjectUpdateAppServiceBuilder.create_service()
        return self._project_update_app_service

    @property
    def project_get_app_service(self) -> ProjectGetAppService:
        if self._project_get_app_service is None:
            self._project_get_app_service = ProjectGetAppServiceBuilder.create_service()
        return self._project_get_app_service

    @property
    def project_delete_app_service(self) -> ProjectDeleteAppService:
        if self._project_delete_app_service is None:
            self._project_delete_app_service = ProjectDeleteAppServiceBuilder.create_service()
        return self._project_delete_app_service

    @property
    def project_image_app_service(self) -> ProjectImageAppService:
        if self._project_image_app_service is None:
            self._project_image_app_service = ProjectImageAppServiceBuilder.create_service()
        return self._project_image_app_service

    @property
    def user_favorite_app_service(self) -> UserFavoriteAppService:
        if self._user_favorite_app_service is None:
            self._user_favorite_app_service = UserFavoriteAppAppServiceBuilder.create_service()
        return self._user_favorite_app_service

    @property
    def news_app_service(self) -> NewsAppService:
        if self._news_app_service is None:
            self._news_app_service = NewsAppServiceBuilder.create_service()
        return self._news_app_service

    @property
    def company_app_service(self) -> CompanyAppService:
        if self._company_app_service is None:
            self._company_app_service = CompanyAppServiceBuilder.create_service()
        return self._company_app_service

    @property
    def accelerator_app_service(self) -> AcceleratorAppService:
        if self._accelerator_app_service is None:
            self._accelerator_app_service = AcceleratorAppServiceBuilder.create_service()
        return self._accelerator_app_service

    @property
    def crowdfunding_app_service(self) -> CrowdfundingAppService:
        if self._crowdfunding_app_service is None:
            self._crowdfunding_app_service = CrowdfundingAppServiceBuilder.create_service()
        return self._crowdfunding_app_service

    @property
    def project_investment_app_service(self) -> ProjectInvestmentAppService:
        if self._project_investment_app_service is None:
            self._project_investment_app_service = ProjectInvestmentAppServiceBuilder.create_service()
        return self._project_investment_app_service

    @property
    def project_investment_social_link_app_service(self) -> ProjectInvestmentSocialLinkAppService:
        if self._project_investment_social_link_app_service is None:
            self._project_investment_social_link_app_service = (
                ProjectInvestmentSocialLinkAppServiceBuilder.create_service()
            )
        return self._project_investment_social_link_app_service

    @property
    def project_investment_phone_app_service(self) -> ProjectInvestmentPhoneAppService:
        if self._project_investment_phone_app_service is None:
            self._project_investment_phone_app_service = ProjectInvestmentPhoneAppServiceBuilder.create_service()
        return self._project_investment_phone_app_service

    @property
    def project_government_grant_app_service(self) -> GovernmentGrantAppService:
        if self._proejct_government_grant_app_service is None:
            self._proejct_government_grant_app_service = GovernmentGrantAppServiceBuilder.create_service()
        return self._proejct_government_grant_app_service

    @property
    def project_bootstrap_app_service(self) -> ProjectBootstrapAppService:
        if self._project_bootstrap_app_service is None:
            self._project_bootstrap_app_service = ProjectBootstrapAppServiceBuilder.create_service()
        return self._project_bootstrap_app_service

    @property
    def project_bank_loan_app_service(self) -> ProjectBankLoanAppService:
        if self._project_bank_load_app_service is None:
            self._project_bank_load_app_service = ProjectBankLoanAppServiceBuilder.create_service()
        return self._project_bank_load_app_service

    @property
    def project_file_app_service(self) -> ProjectFileAppService:
        if self._project_file_app_service is None:
            self._project_file_app_service = ProjectFileAppServiceBuilder.create_service()
        return self._project_file_app_service

    @property
    def project_media_app_service(self) -> ProjectMediaAppService:
        if self._project_media_app_service is None:
            self._project_media_app_service = ProjectMediaAppServiceBuilder.create_service()
        return self._project_media_app_service

    @property
    def region_app_service(self) -> RegionAppService:
        if self._region_app_service is None:
            self._region_app_service = RegionAppServiceBuilder.create_service()
        return self._region_app_service

    @property
    def city_app_service(self) -> CityAppService:
        if self._city_app_service is None:
            self._city_app_service = CityAppServiceBuilder.create_service()
        return self._city_app_service

    @property
    def project_useful_link_app_service(self) -> ProjectUsefulLinkAppService:
        if self._project_useful_link_app_service is None:
            self._project_useful_link_app_service = ProjectUsefulLinkAppServiceBuilder.create_service()
        return self._project_useful_link_app_service

    @property
    def projects_admin_app_service(self) -> ProjectAdminAppService:
        if self._project_admin_app_service is None:
            self._project_admin_app_service = ProjectAdminAppServiceBuilder.create_service()
        return self._project_admin_app_service

    @property
    def user_admin_app_service(self) -> UserAdminAppService:
        if self._user_admin_app_service is None:
            self._user_admin_app_service = UserAdminAppServiceBuilder.create_service()
        return self._user_admin_app_service

    @property
    def notification_app_service(self) -> NotificationAppService:
        if self._notification_app_service is None:
            self._notification_app_service = NotificationAppServiceBuilder.create_service()

        return self._notification_app_service

    @property
    def cookie_service(self) -> CookieService:
        if self._cookie_service is None:
            self._cookie_service = cookie_service
        return self._cookie_service


gateway = Gateway()
