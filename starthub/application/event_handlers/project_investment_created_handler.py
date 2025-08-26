from domain.events.project import ProjectInvestmentCreatedEvent
from domain.models.project_management.project import Project
from domain.models.user_management.user import User
from domain.ports.event import AbstractEventHandler
from domain.services.project_management.investment import ProjectInvestmentSocialLinkService
from domain.value_objects.common import SocialLink
from domain.value_objects.project.investment import ProjectInvestmentId
from domain.value_objects.project.project_investment_social_link import ProjectInvestmentSocialLinkCreatePayload
from loguru import logger


class ProjectInvestmentCreatedEventHandler(AbstractEventHandler[ProjectInvestmentCreatedEvent]):
    def __init__(
        self,
        project_investment_social_link_service: ProjectInvestmentSocialLinkService,
    ):
        self._project_investment_social_link_service = project_investment_social_link_service

    def handle(self, event: ProjectInvestmentCreatedEvent) -> None:
        social_links = event.social_links
        investment = event.project_investment
        user = event.user
        project = event.project

        self._create_social_links(
            user=user,
            project=project,
            social_links=social_links,
            investment_id=ProjectInvestmentId(value=investment.id),
        )

    def _create_social_links(
        self, user: User, project: Project, social_links: list[SocialLink], investment_id: ProjectInvestmentId
    ) -> None:
        for sl in social_links:
            investment_social_link = self._project_investment_social_link_service.create(
                user=user,
                project=project,
                payload=ProjectInvestmentSocialLinkCreatePayload(
                    investment_id=investment_id,
                    social_link=sl,
                ),
            )
            logger.debug(f"Project investment social link with id = {investment_social_link.id} created.")
        logger.info("All social links are created successfully.")
