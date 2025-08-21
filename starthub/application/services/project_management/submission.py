from application.ports.service import AbstractAppService
from domain.repositories.project.project import ProjectReadRepository
from domain.repositories.user import UserReadRepository
from domain.services.project_management.submission import ProjectSubmissionService
from domain.value_objects.common import Id
from loguru import logger


class ProjectSubmissionAppService(AbstractAppService):
    def __init__(
        self,
        project_submission_service: ProjectSubmissionService,
        user_read_repository: UserReadRepository,
        project_read_repository: ProjectReadRepository,
    ):
        self._project_submission_service = project_submission_service
        self._user_read_repository = user_read_repository
        self._project_read_repository = project_read_repository

    def approve(self, user_id: Id, project_id: Id) -> None:
        logger.info(f"User(id={user_id.value}) is approving submission for the Project(id={project_id.value}).")

        user = self._user_read_repository.get_by_id(id_=user_id)
        project = self._project_read_repository.get_by_id(id_=project_id)

        self._project_submission_service.approve(user=user, project=project)

    def reject(self, user_id: Id, project_id: Id) -> None:
        logger.info(f"User(id={user_id.value}) is rejecting submission for the Project(id={project_id.value}).")

        user = self._user_read_repository.get_by_id(id_=user_id)
        project = self._project_read_repository.get_by_id(id_=project_id)

        self._project_submission_service.reject(user=user, project=project)
