from loguru import logger

from application.ports.service import AbstractAppService
from domain.models.project_management.bootstrap import ProjectBootstrap
from domain.models.project_management.project import Project
from domain.models.user import User
from domain.repositories.project.bootstrap import ProjectBootstrapReadRepository
from domain.repositories.project.project import ProjectReadRepository
from domain.repositories.user import UserReadRepository
from domain.services.project_management.bootsrtap import ProjectBootstrapService
from domain.value_objects.common import Id
from domain.value_objects.project.bootstrap import (
    ProjectBootstrapCreateCommand,
    ProjectBootstrapCreatePayload,
    ProjectBootstrapId,
    ProjectBootstrapUpdateCommand,
    ProjectBootstrapUpdatePayload,
)


class ProjectBootstrapAppService(AbstractAppService):
    def __init__(
        self,
        bootstrap_service: ProjectBootstrapService,
        bootstrap_read_repository: ProjectBootstrapReadRepository,
        user_read_repository: UserReadRepository,
        project_read_repository: ProjectReadRepository,
    ):
        self._bootstrap_service = bootstrap_service
        self._bootstrap_read_repository = bootstrap_read_repository
        self._user_read_repository = user_read_repository
        self._project_read_repository = project_read_repository

    def create(self, user_id: Id, project_id: Id, command: ProjectBootstrapCreateCommand) -> None:
        """
        :raises UserNotFoundException:
        :raises ProjectNotFoundException:
        """
        user: User = self._user_read_repository.get_by_id(id_=user_id)
        project: Project = self._project_read_repository.get_by_id(id_=project_id)
        self._bootstrap_service.create(
            user=user,
            project=project,
            payload=ProjectBootstrapCreatePayload(project_id=project_id, description=command.description),
        )
        logger.info(f"Bootstrap for the Project(id={project_id.value}) created successfully.")

    def update(self, user_id: Id, bootstrap_id: ProjectBootstrapId, command: ProjectBootstrapUpdateCommand) -> None:
        user: User = self._user_read_repository.get_by_id(id_=user_id)
        bootstrap: ProjectBootstrap = self._bootstrap_read_repository.get_by_id(id_=bootstrap_id)
        self._bootstrap_service.update(
            user=user,
            bootstrap=bootstrap,
            payload=ProjectBootstrapUpdatePayload(
                bootstrap_id=bootstrap_id,
                description=command.description,
            ),
        )
        logger.info("ProjectBootstrap updated successfully.")

    def delete(self, user_id: Id, bootstrap_id: ProjectBootstrapId) -> None:
        user: User = self._user_read_repository.get_by_id(id_=user_id)
        bootstrap: ProjectBootstrap = self._bootstrap_read_repository.get_by_id(id_=bootstrap_id)
        self._bootstrap_service.delete(user=user, bootstrap=bootstrap)
