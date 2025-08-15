from application.ports.service import AbstractAppService
from domain.repositories.project.media import ProjectMediaReadRepository
from domain.repositories.project.project import ProjectReadRepository
from domain.repositories.user import UserReadRepository
from domain.services.project_management.media import ProjectMediaService
from domain.value_objects.common import Id
from domain.value_objects.project.media import ProjectMediaCreateCommand, ProjectMediaId
from loguru import logger


class ProjectMediaAppService(AbstractAppService):
    def __init__(
        self,
        project_media_service: ProjectMediaService,
        project_media_read_repository: ProjectMediaReadRepository,
        user_read_repository: UserReadRepository,
        project_read_repository: ProjectReadRepository,
    ):
        self._project_media_service = project_media_service
        self._project_media_read_repository = project_media_read_repository
        self._user_read_repository = user_read_repository
        self._project_read_repository = project_read_repository

    def create(self, user_id: Id, project_id: Id, command: ProjectMediaCreateCommand) -> None:
        user = self._user_read_repository.get_by_id(id_=user_id)
        project = self._project_read_repository.get_by_id(id_=project_id)
        self._project_media_service.create(user=user, project=project, command=command)
        logger.info("Project media created successfully.")

    def delete(self, user_id: Id, project_media_id: ProjectMediaId) -> None:
        user = self._user_read_repository.get_by_id(id_=user_id)
        project_media = self._project_media_read_repository.get_by_id(id_=project_media_id)
        self._project_media_service.delete(user=user, project_media=project_media)
        logger.info("Project media deleted successfully.")
