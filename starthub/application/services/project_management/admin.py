from application.dto.project import ProjectDto
from application.ports.service import AbstractAppService
from application.services.project_management.project import ProjectGetAppService
from domain.events.project import ProjectApprovedNotificationEvent, ProjectRejectedEvent
from domain.repositories.project.project import ProjectReadRepository
from domain.repositories.user_management.user import UserReadRepository
from domain.services.project_management.admin import ProjectAdminService
from domain.value_objects.common import Id, Pagination
from domain.value_objects.notification import NotificationMessage, NotificationTitle
from domain.value_objects.project.report import ProjectReportContent
from domain.value_objects.project.submission import ProjectRejectCommand
from infrastructure.event_bus import EventBus
from loguru import logger


class ProjectAdminAppService(AbstractAppService):
    def __init__(
        self,
        project_admin_service: ProjectAdminService,
        user_read_repository: UserReadRepository,
        project_read_repository: ProjectReadRepository,
        project_get_app_service: ProjectGetAppService,
    ):
        self._project_admin_service = project_admin_service
        self._user_read_repository = user_read_repository
        self._project_read_repository = project_read_repository
        self._project_get_app_service = project_get_app_service

    def get_submissions(self, user_id: Id, pagination: Pagination) -> list[ProjectDto]:
        raise NotImplementedError

    def approve_submission(self, user_id: Id, project_id: Id) -> None:
        logger.info(f"User(id={user_id.value}) is approving submission for the Project(id={project_id.value}).")

        user = self._user_read_repository.get_by_id(id_=user_id)
        project = self._project_read_repository.get_by_id(id_=project_id)

        self._project_admin_service.approve_submission(user=user, project=project)

        event = ProjectApprovedNotificationEvent(
            user_id=user_id,
            title=NotificationTitle(value="Your project was approved successfully."),
            message=NotificationMessage(value="Your project was approved successfully."),
        )
        EventBus().publish(event)

    def reject_submission(self, user_id: Id, project_id: Id, command: ProjectRejectCommand) -> None:
        logger.info(f"User(id={user_id.value}) is rejecting submission for the Project(id={project_id.value}).")

        user = self._user_read_repository.get_by_id(id_=user_id)
        project = self._project_read_repository.get_by_id(id_=project_id)

        self._project_admin_service.reject_submission(user=user, project=project)

        event = ProjectRejectedEvent(
            project_id=project_id,
            user_id=user_id,
            report=ProjectReportContent(value=command.report.value),
        )
        EventBus().publish(event)

    def deactivate(self, user_id: Id, project_id: Id) -> None:
        logger.info(f"User(id={user_id.value}) is deactivating the Project(id={project_id.value}).")

        user = self._user_read_repository.get_by_id(id_=user_id)
        project = self._project_read_repository.get_by_id(id_=project_id)

        self._project_admin_service.deactivate(user=user, project=project)
