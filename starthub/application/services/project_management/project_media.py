from application.ports.service import AbstractAppService
from domain.repositories.project.project import ProjectReadRepository
from domain.repositories.user import UserReadRepository
from domain.services.project_management.media import ProjectMediaService
from domain.value_objects.common import Id
from domain.value_objects.project.media import ProjectMediaCreateCommand


class ProjectMediaAppService(AbstractAppService):
    def __init__(
        self,
        project_media_service: ProjectMediaService,
        user_read_repository: UserReadRepository,
        project_read_repository: ProjectReadRepository,
    ):
        self._project_media_service = project_media_service
        self._user_read_repository = user_read_repository
        self._project_read_repository = project_read_repository

    def create(self, user_id: Id, project_id: Id, command: ProjectMediaCreateCommand) -> None:
        user = self._user_read_repository.get_by_id(id_=user_id)
        project = self._project_read_repository.get_by_id(id_=project_id)
        self._project_media_service.create(user=user, project=project, command=command)
