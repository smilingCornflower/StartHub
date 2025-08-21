from application.ports.service import AbstractAppService
from domain.repositories.project.project import ProjectReadRepository
from domain.repositories.user import UserReadRepository
from domain.services.project_management.admin import ProjectAdminService
from domain.value_objects.common import Id
from loguru import logger


class ProjectAdminAppService(AbstractAppService):
    def __init__(
        self,
        project_admin_service: ProjectAdminService,
        user_read_repository: UserReadRepository,
        project_read_repository: ProjectReadRepository,
    ):
        self._project_admin_service = project_admin_service
        self._user_read_repository = user_read_repository
        self._project_read_repository = project_read_repository

    def approve_submission(self, user_id: Id, project_id: Id) -> None:
        logger.info(f"User(id={user_id.value}) is approving submission for the Project(id={project_id.value}).")

        user = self._user_read_repository.get_by_id(id_=user_id)
        project = self._project_read_repository.get_by_id(id_=project_id)

        self._project_admin_service.approve_submission(user=user, project=project)

    def reject_submission(self, user_id: Id, project_id: Id) -> None:
        logger.info(f"User(id={user_id.value}) is rejecting submission for the Project(id={project_id.value}).")

        user = self._user_read_repository.get_by_id(id_=user_id)
        project = self._project_read_repository.get_by_id(id_=project_id)

        self._project_admin_service.reject_submission(user=user, project=project)

    def deactivate(self, user_id: Id, project_id: Id) -> None:
        logger.info(f"User(id={user_id.value}) is deactivating the Project(id={project_id.value}).")

        user = self._user_read_repository.get_by_id(id_=user_id)
        project = self._project_read_repository.get_by_id(id_=project_id)

        self._project_admin_service.deactivate(user=user, project=project)
