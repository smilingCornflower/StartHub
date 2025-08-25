from application.ports.service import AbstractAppService
from domain.repositories.project.project import ProjectReadRepository
from domain.repositories.user_management.user import UserReadRepository
from domain.services.project_management.resubmit import ProjectResubmitService
from domain.value_objects.common import Id


class ProjectResubmitAppService(AbstractAppService):
    def __init__(
        self,
        project_resubmit_service: ProjectResubmitService,
        user_read_repository: UserReadRepository,
        project_read_repository: ProjectReadRepository,
    ):
        self._project_resubmit_service = project_resubmit_service
        self._user_read_repository = user_read_repository
        self._project_read_repository = project_read_repository

    def resubmit(self, user_id: Id, project_id: Id) -> None:
        user = self._user_read_repository.get_by_id(id_=user_id)
        project = self._project_read_repository.get_by_id(id_=project_id)

        self._project_resubmit_service.resubmit(user=user, project=project)
