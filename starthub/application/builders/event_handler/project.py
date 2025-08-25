from typing import Any

from application.builders.app_service.project_management.accelerator import AcceleratorAppServiceBuilder
from application.builders.app_service.project_management.bank_loan import ProjectBankLoanAppServiceBuilder
from application.builders.app_service.project_management.bootstrap import ProjectBootstrapAppServiceBuilder
from application.builders.app_service.project_management.crowdfunding import CrowdfundingAppServiceBuilder
from application.builders.app_service.project_management.government_grant import GovernmentGrantAppServiceBuilder
from application.builders.app_service.project_management.investment import ProjectInvestmentAppServiceBuilder
from application.builders.app_service.project_management.project_file import ProjectFileAppServiceBuilder
from application.builders.app_service.project_management.project_media import ProjectMediaAppServiceBuilder
from application.builders.app_service.project_management.useful_link import ProjectUsefulLinkAppServiceBuilder
from application.builders.domain_service.address import AddressServiceBuilder
from application.builders.domain_service.project_management import (
    CompanyFounderServiceBuilder,
    CompanyServiceBuilder,
    ProjectIncubatorServiceBuilder,
    ProjectPhoneServiceBuilder,
    ProjectReportServiceBuilder,
    ProjectSocialLinkServiceBuilder,
    ProjectStepServiceBuilder,
)
from application.event_handlers.project_created.accelerator_handler import ProjectCreatedAcceleratorHandler
from application.event_handlers.project_created.bank_loan_handler import ProjectCreatedBankLoanHandler
from application.event_handlers.project_created.bootstrap import ProjectCreatedBootstrapHandler
from application.event_handlers.project_created.company_handler import ProjectCreatedCompanyHandler
from application.event_handlers.project_created.crowdfunding_handler import ProjectCreatedCrowdfundingHandler
from application.event_handlers.project_created.government_grant_handler import ProjectCreatedGovernmentGrantHandler
from application.event_handlers.project_created.incubator_handler import ProjectCreatedIncubatorHandler
from application.event_handlers.project_created.investment_handler import ProjectCreatedInvestmentHandler
from application.event_handlers.project_created.media_handler import ProjectCreatedProjectMediaHandler
from application.event_handlers.project_created.project_file_handler import ProjectCreatedProjectFileHandler
from application.event_handlers.project_created.project_phone_handler import ProjectCreatedPhoneHandler
from application.event_handlers.project_created.project_step_handler import ProjectCreatedProjectStepsHandler
from application.event_handlers.project_created.social_link_handler import ProjectCreatedSocialLinkHandler
from application.event_handlers.project_created.useful_link_handler import ProjectCreatedUsefulLinkHandler
from application.event_handlers.project_deleted_handler import ProjectDeletedEventHandler
from application.event_handlers.project_rejected_handler import ProjectRejectedReportEventHandler
from application.ports.event_handler_builder import AbstractEventHandlerBuilder
from domain.events.project import ProjectCreatedEvent, ProjectDeletedEvent
from domain.ports.event import AbstractEventHandler
from infrastructure.cloud_storages.google import google_cloud_storage


class ProjectCreatedAcceleratorHandlerBuilder(AbstractEventHandlerBuilder[Any]):
    @staticmethod
    def create_handler() -> AbstractEventHandler[ProjectCreatedEvent]:
        return ProjectCreatedAcceleratorHandler(accelerator_app_service=AcceleratorAppServiceBuilder.create_service())


class ProjectCreatedBootstrapHandlerBuilder(AbstractEventHandlerBuilder[Any]):
    @staticmethod
    def create_handler() -> AbstractEventHandler[ProjectCreatedEvent]:
        return ProjectCreatedBootstrapHandler(bootstrap_app_service=ProjectBootstrapAppServiceBuilder.create_service())


class ProjectCreatedCompanyHandlerBuilder(AbstractEventHandlerBuilder[Any]):
    @staticmethod
    def create_handler() -> AbstractEventHandler[ProjectCreatedEvent]:
        return ProjectCreatedCompanyHandler(
            company_service=CompanyServiceBuilder.create_service(),
            company_founder_service=CompanyFounderServiceBuilder.create_service(),
            address_service=AddressServiceBuilder.create_service(),
        )


class ProjectCreatedCrowdfundingHandlerBuilder(AbstractEventHandlerBuilder[Any]):
    @staticmethod
    def create_handler() -> AbstractEventHandler[ProjectCreatedEvent]:
        return ProjectCreatedCrowdfundingHandler(
            crowdfunding_app_service=CrowdfundingAppServiceBuilder.create_service()
        )


class ProjectCreatedGovernmentGrantHandlerBuilder(AbstractEventHandlerBuilder[Any]):
    @staticmethod
    def create_handler() -> AbstractEventHandler[ProjectCreatedEvent]:
        return ProjectCreatedGovernmentGrantHandler(
            government_grant_app_service=GovernmentGrantAppServiceBuilder.create_service()
        )


class ProjectCreatedIncubatorHandlerBuilder(AbstractEventHandlerBuilder[Any]):
    @staticmethod
    def create_handler() -> AbstractEventHandler[ProjectCreatedEvent]:
        return ProjectCreatedIncubatorHandler(incubator_service=ProjectIncubatorServiceBuilder.create_service())


class ProjectCreatedInvestmentHandlerBuilder(AbstractEventHandlerBuilder[Any]):
    @staticmethod
    def create_handler() -> AbstractEventHandler[ProjectCreatedEvent]:
        return ProjectCreatedInvestmentHandler(
            investment_app_service=ProjectInvestmentAppServiceBuilder.create_service()
        )


class ProjectCreatedPhoneHandlerBuilder(AbstractEventHandlerBuilder[Any]):
    @staticmethod
    def create_handler() -> AbstractEventHandler[ProjectCreatedEvent]:
        return ProjectCreatedPhoneHandler(project_phone_service=ProjectPhoneServiceBuilder.create_service())


class ProjectCreatedProjectStepHandlerBuilder(AbstractEventHandlerBuilder[Any]):
    @staticmethod
    def create_handler() -> AbstractEventHandler[ProjectCreatedEvent]:
        return ProjectCreatedProjectStepsHandler(project_step_service=ProjectStepServiceBuilder.create_service())


class ProjectCreatedSocialLinkHandlerBuilder(AbstractEventHandlerBuilder[Any]):
    @staticmethod
    def create_handler() -> AbstractEventHandler[ProjectCreatedEvent]:
        return ProjectCreatedSocialLinkHandler(
            project_social_link_service=ProjectSocialLinkServiceBuilder.create_service()
        )


class ProjectCreatedBankLoanHandlerBuilder(AbstractEventHandlerBuilder[Any]):
    @staticmethod
    def create_handler() -> ProjectCreatedBankLoanHandler:
        return ProjectCreatedBankLoanHandler(bank_loan_app_service=ProjectBankLoanAppServiceBuilder.create_service())


class ProjectCreatedProjectFileHandlerBuilder(AbstractEventHandlerBuilder[Any]):
    @staticmethod
    def create_handler() -> ProjectCreatedProjectFileHandler:
        return ProjectCreatedProjectFileHandler(project_file_app_servcie=ProjectFileAppServiceBuilder.create_service())


class ProjectCreatedProjectMediaHandlerBuilder(AbstractEventHandlerBuilder[Any]):
    @staticmethod
    def create_handler() -> ProjectCreatedProjectMediaHandler:
        return ProjectCreatedProjectMediaHandler(
            project_media_app_service=ProjectMediaAppServiceBuilder.create_service()
        )


class ProjectCreatedUsefulLinkHandlerBuilder(AbstractEventHandlerBuilder[Any]):
    @staticmethod
    def create_handler() -> ProjectCreatedUsefulLinkHandler:
        return ProjectCreatedUsefulLinkHandler(
            project_useful_link_app_service=ProjectUsefulLinkAppServiceBuilder.create_service()
        )


class ProjectDeletedEventHandlerBuilder(AbstractEventHandlerBuilder[Any]):
    @staticmethod
    def create_handler() -> AbstractEventHandler[ProjectDeletedEvent]:
        return ProjectDeletedEventHandler(
            cloud_storage=google_cloud_storage,
        )


class ProjectRejectedReportEventHandlerBuilder(AbstractEventHandlerBuilder[Any]):
    @staticmethod
    def create_handler() -> ProjectRejectedReportEventHandler:
        return ProjectRejectedReportEventHandler(
            project_report_service=ProjectReportServiceBuilder.create_service(),
        )
