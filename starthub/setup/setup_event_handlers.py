from application.builders.event_handler.project import (
    ProjectCreatedAcceleratorHandlerBuilder,
    ProjectCreatedBankLoanHandlerBuilder,
    ProjectCreatedBootstrapHandlerBuilder,
    ProjectCreatedCompanyHandlerBuilder,
    ProjectCreatedCrowdfundingHandlerBuilder,
    ProjectCreatedGovernmentGrantHandlerBuilder,
    ProjectCreatedImageHandlerBuilder,
    ProjectCreatedIncubatorHandlerBuilder,
    ProjectCreatedInvestmentHandlerBuilder,
    ProjectCreatedPhoneHandlerBuilder,
    ProjectCreatedProjectStepHandlerBuilder,
    ProjectCreatedSocialLinkHandlerBuilder,
    ProjectDeletedEventHandlerBuilder,
)
from application.builders.event_handler.project_investment import ProjectInvestmentCreatedEventHandlerBuilder
from domain.enums.event import EventType
from infrastructure.event_bus import EventBus
from loguru import logger


def setup_project_created_handlers() -> None:
    bus = EventBus()
    accelerator_handler = ProjectCreatedAcceleratorHandlerBuilder.create_handler()
    bootstrap_handler = ProjectCreatedBootstrapHandlerBuilder.create_handler()
    company_handler = ProjectCreatedCompanyHandlerBuilder.create_handler()
    crowdfunding_handler = ProjectCreatedCrowdfundingHandlerBuilder.create_handler()
    government_grant_handler = ProjectCreatedGovernmentGrantHandlerBuilder.create_handler()
    incubator_handler = ProjectCreatedIncubatorHandlerBuilder.create_handler()
    investment_handler = ProjectCreatedInvestmentHandlerBuilder.create_handler()
    image_handler = ProjectCreatedImageHandlerBuilder.create_handler()
    phone_handler = ProjectCreatedPhoneHandlerBuilder.create_handler()
    project_step_handler = ProjectCreatedProjectStepHandlerBuilder.create_handler()
    social_link_handler = ProjectCreatedSocialLinkHandlerBuilder.create_handler()
    bank_loan_handler = ProjectCreatedBankLoanHandlerBuilder.create_handler()

    handlers = [
        accelerator_handler,
        bootstrap_handler,
        company_handler,
        crowdfunding_handler,
        government_grant_handler,
        incubator_handler,
        investment_handler,
        image_handler,
        phone_handler,
        project_step_handler,
        social_link_handler,
        bank_loan_handler,
    ]
    for i in handlers:
        bus.subscribe(event_type=EventType.Project.CREATED, handler=i)


def setup_event_handlers() -> None:
    logger.warning("Started setup event handlers.")
    bus = EventBus()

    setup_project_created_handlers()
    project_deleted_handler = ProjectDeletedEventHandlerBuilder.create_handler()
    project_investment_created_handler = ProjectInvestmentCreatedEventHandlerBuilder.create_handler()

    bus.subscribe(event_type=EventType.Project.DELETED, handler=project_deleted_handler)
    bus.subscribe(event_type=EventType.ProjectInvestment.CREATED, handler=project_investment_created_handler)

    logger.info("Event handlers successfully registered.")
