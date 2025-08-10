from loguru import logger

from application.ports.service import AbstractAppService
from domain.models.project_management.crowdfunding import ProjectCrowdfunding
from domain.models.user import User
from domain.repositories.project.crowdfunding import ProjectCrowdfundingReadRepository
from domain.repositories.user import UserReadRepository
from domain.services.project_management.crowdfunding import ProjectCrowdfundingService
from domain.value_objects.common import Id
from domain.value_objects.project.crowdfunding import ProjectCrowdfundingId


class CrowdfundingAppService(AbstractAppService):
    def __init__(
            self,
            read_repository: ProjectCrowdfundingReadRepository,
            crowdfunding_service: ProjectCrowdfundingService,
            user_read_repository: UserReadRepository,
    ):
        self._read_repository = read_repository
        self._crowdfunding_service = crowdfunding_service
        self._user_read_repository = user_read_repository

    def delete(self, user_id: Id, crowdfunding_id: ProjectCrowdfundingId) -> None:
        """:raises UserNotFoundException:"""

        user: User = self._user_read_repository.get_by_id(id_=user_id)
        crowdfunding: ProjectCrowdfunding = self._read_repository.get_by_id(id_=crowdfunding_id)
        logger.debug("User and Corwdfunding are exist.")
        self._crowdfunding_service.delete(user=user, crowdfunding=crowdfunding)
        logger.info(f"ProjectCrowdfunding(id={crowdfunding_id.value} deleted successfully.)")
