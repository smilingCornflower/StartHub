from application.ports.service import AbstractAppService
from domain.exceptions.project_management import (
    ProjectCrowdfundingAlreadyExistsException,
    ProjectCrowdfundingNotFoundException,
)
from domain.models.project_management.crowdfunding import ProjectCrowdfunding
from domain.models.project_management.project import Project
from domain.models.user import User
from domain.repositories.project.crowdfunding import ProjectCrowdfundingReadRepository
from domain.repositories.project.project import ProjectReadRepository
from domain.repositories.user import UserReadRepository
from domain.services.project_management.crowdfunding import ProjectCrowdfundingService
from domain.value_objects.common import Id
from domain.value_objects.filter import ProjectCrowdfundingFilter
from domain.value_objects.project.crowdfunding import (
    ProjectCrowdfundingCreateCommand,
    ProjectCrowdfundingCreatePayload,
    ProjectCrowdfundingUpdateCommand,
    ProjectCrowdfundingUpdatePayload,
)
from loguru import logger


class CrowdfundingAppService(AbstractAppService):
    def __init__(
        self,
        crowdfunding_service: ProjectCrowdfundingService,
        read_repository: ProjectCrowdfundingReadRepository,
        user_read_repository: UserReadRepository,
        project_read_repository: ProjectReadRepository,
    ):
        self._crowdfunding_service = crowdfunding_service
        self._read_repository = read_repository
        self._user_read_repository = user_read_repository
        self._project_read_repository = project_read_repository

    def create(self, user_id: Id, project_id: Id, command: ProjectCrowdfundingCreateCommand) -> None:
        """
        :raises ProjectCrowdfundingAlreadyExistsException:
        :raises UserNotFoundExcpetion:
        :raises ProjectNotFoundException:
        """
        crowdfundings: list[ProjectCrowdfunding] = self._read_repository.get_all(
            filter_=ProjectCrowdfundingFilter(project_id=project_id)
        )
        if crowdfundings:
            raise ProjectCrowdfundingAlreadyExistsException(
                f"Crowdfunding for the project with id = {project_id.value} already exists."
            )

        user: User = self._user_read_repository.get_by_id(id_=user_id)
        project: Project = self._project_read_repository.get_by_id(id_=project_id)

        self._crowdfunding_service.create(
            user=user,
            project=project,
            payload=ProjectCrowdfundingCreatePayload(
                project_id=project_id,
                name=command.name,
                amount=command.amount,
            ),
        )

    def delete(self, user_id: Id, project_id: Id) -> None:
        """:raises UserNotFoundException:"""

        user: User = self._user_read_repository.get_by_id(id_=user_id)
        crowdfundings: list[ProjectCrowdfunding] = self._read_repository.get_all(
            filter_=ProjectCrowdfundingFilter(project_id=project_id)
        )
        if crowdfundings:
            crowdfunding = crowdfundings[0]
            logger.debug("User and Corwdfunding are exist.")
            self._crowdfunding_service.delete(user=user, crowdfunding=crowdfunding)
            logger.info(f"ProjectCrowdfunding for the Project(id={project_id.value}) deleted successfully.)")
        else:
            logger.exception(f"ProjectCrowdfunding doesn't exists for the Project(id={project_id.value})")
            raise ProjectCrowdfundingNotFoundException(
                f"ProjectCrowdfunding for the project with id = {project_id.value} doesn't exists."
            )

    def update(self, user_id: Id, project_id: Id, command: ProjectCrowdfundingUpdateCommand) -> None:
        user: User = self._user_read_repository.get_by_id(id_=user_id)
        crowdfundings: list[ProjectCrowdfunding] = self._read_repository.get_all(
            filter_=ProjectCrowdfundingFilter(project_id=project_id)
        )
        if crowdfundings:
            logger.debug("User and Corwdfunding are exist.")
            self._crowdfunding_service.update(
                user=user,
                crowdfunding=crowdfundings[0],
                payload=ProjectCrowdfundingUpdatePayload(
                    project_id=project_id,
                    name=command.name,
                    amount=command.amount,
                ),
            )
            logger.info("Crowdfunding updated successfully.")
        else:
            logger.exception(f"ProjectCrowdfunding doesn't exists for the Project(id={project_id.value})")
            raise ProjectCrowdfundingNotFoundException(
                f"ProjectCrowdfunding for the project with id = {project_id.value} doesn't exists."
            )
