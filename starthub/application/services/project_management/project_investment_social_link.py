from loguru import logger

from application.ports.service import AbstractAppService
from domain.models.project_management.investment import ProjectInvestment
from domain.models.project_management.project import Project
from domain.models.user import User
from domain.repositories.project.investment import (
    ProjectInvestmentReadRepository,
    ProjectInvestmentSocialLinkReadRepository,
)
from domain.repositories.project.project import ProjectReadRepository
from domain.repositories.user import UserReadRepository
from domain.services.project_management.investment import ProjectInvestmentSocialLinkService
from domain.value_objects.common import Id, SocialLink
from domain.value_objects.project.investment import ProjectInvestmentId
from domain.value_objects.project.project_investment_social_link import (
    ProjectInvestmentSocialLinkCreatePayload,
    ProjectInvestmentSocialLinkId,
)


class ProjectInvestmentSocialLinkAppService(AbstractAppService):
    def __init__(
        self,
        project_investment_social_link_service: ProjectInvestmentSocialLinkService,
        project_investment_social_link_read_repository: ProjectInvestmentSocialLinkReadRepository,
        user_read_repository: UserReadRepository,
        project_read_repository: ProjectReadRepository,
        project_investment_read_repository: ProjectInvestmentReadRepository,
    ):
        self._project_investment_social_link_service = project_investment_social_link_service
        self._project_investment_social_link_read_repository = project_investment_social_link_read_repository
        self._user_read_repository = user_read_repository
        self._project_read_repository = project_read_repository
        self._project_investment_read_repository = project_investment_read_repository

    def create(self, user_id: Id, investment_id: ProjectInvestmentId, social_links: list[SocialLink]) -> None:
        """
        :raises UserNotFoundException:
        :raises ProjectNotFoundException:
        :raises ProjectInvestmentNotFoundException:
        :raises ProjectInvestmentDoesNotBelongToProjectExceptino:
        """
        user: User = self._user_read_repository.get_by_id(id_=user_id)
        investment: ProjectInvestment = self._project_investment_read_repository.get_by_id(id_=investment_id)
        project: Project = self._project_read_repository.get_by_id(id_=Id(value=investment.project_id))

        for sl in social_links:
            social_link = self._project_investment_social_link_service.create(
                user=user,
                project=project,
                payload=ProjectInvestmentSocialLinkCreatePayload(
                    investment_id=investment_id,
                    social_link=sl,
                ),
            )
            logger.debug(f"SocialLink created with id = {social_link.id}")
        logger.info("All social links are created.")

    def delete(self, user_id: Id, social_link_id: ProjectInvestmentSocialLinkId) -> None:
        user: User = self._user_read_repository.get_by_id(id_=user_id)

        social_link = self._project_investment_social_link_read_repository.get_by_id(id_=social_link_id)
        investment: ProjectInvestment = self._project_investment_read_repository.get_by_id(
            id_=ProjectInvestmentId(value=social_link.investment_id)
        )
        project: Project = self._project_read_repository.get_by_id(id_=Id(value=investment.project_id))

        self._project_investment_social_link_service.delete(user=user, project=project, social_link=social_link)
