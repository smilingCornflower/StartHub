from application.ports.service import AbstractAppService
from domain.models.project_management.project import Project
from domain.models.user import User
from domain.repositories.project.project import ProjectReadRepository
from domain.repositories.project.project_file import ProjectFileReadRepository
from domain.repositories.user import UserReadRepository
from domain.services.project_management.project_file import ProjectFileService
from domain.value_objects.common import Id
from domain.value_objects.project.project_file import ProjectFileCreateCommand, ProjectFileId


class ProjectFileAppService(AbstractAppService):
    def __init__(
        self,
        project_file_service: ProjectFileService,
        project_file_read_repository: ProjectFileReadRepository,
        user_read_repository: UserReadRepository,
        project_read_repository: ProjectReadRepository,
    ):
        self._project_file_service = project_file_service
        self._project_file_read_repository = project_file_read_repository
        self._user_read_repository = user_read_repository
        self._project_read_repository = project_read_repository

    def create(self, user_id: Id, project_id: Id, command: ProjectFileCreateCommand) -> None:
        user: User = self._user_read_repository.get_by_id(id_=user_id)
        project: Project = self._project_read_repository.get_by_id(id_=project_id)

        self._project_file_service.create(user=user, project=project, command=command)

    def delete(self, user_id: Id, project_file_id: ProjectFileId) -> None:
        user: User = self._user_read_repository.get_by_id(id_=user_id)
        project_file = self._project_file_read_repository.get_by_id(id_=project_file_id)

        self._project_file_service.delete(user=user, project_file=project_file)
