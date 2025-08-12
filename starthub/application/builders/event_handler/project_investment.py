from typing import Any

from application.builders.domain_service.project_management import ProjectInvestmentSocialLinkServiceBuilder
from application.event_handlers.project_investment_created_handler import ProjectInvestmentCreatedEventHandler
from application.ports.event_handler_builder import AbstractEventHandlerBuilder


class ProjectInvestmentCreatedEventHandlerBuilder(AbstractEventHandlerBuilder[Any]):
    @staticmethod
    def create_handler() -> ProjectInvestmentCreatedEventHandler:
        return ProjectInvestmentCreatedEventHandler(
            project_investment_social_link_service=ProjectInvestmentSocialLinkServiceBuilder.create_service(),
        )
