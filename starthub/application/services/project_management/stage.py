from application.ports.service import AbstractAppService
from domain.repositories.project.stage import ProjectStageReadRepository
from domain.repositories.user_management.user import UserReadRepository
from domain.services.project_management.stage import ProjectStageService
from domain.value_objects.common import Id
from domain.value_objects.project.stage import ProjectStageId, ProjectStageUpdateCommand, ProjectStageUpdatePayload


class ProjectStageAppService(AbstractAppService):
    def __init__(
        self,
        stage_service: ProjectStageService,
        user_read_repository: UserReadRepository,
        project_stage_read_reposiotry: ProjectStageReadRepository,
    ):
        self._stage_service = stage_service
        self._user_read_repository = user_read_repository
        self._project_stage_read_reposiotry = project_stage_read_reposiotry

    def update(self, user_id: Id, stage_id: ProjectStageId, command: ProjectStageUpdateCommand) -> None:
        user = self._user_read_repository.get_by_id(id_=user_id)
        self._project_stage_read_reposiotry.get_by_id(id_=stage_id)
        self._stage_service.update(
            user=user, payload=ProjectStageUpdatePayload(id_=stage_id, description=command.description)
        )
