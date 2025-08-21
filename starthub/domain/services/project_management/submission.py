from domain.enums.permission import ActionEnum, ScopeEnum
from domain.enums.project_status import ProjectStatusEnum
from domain.exceptions.permissions import UpdateDeniedPermissionException
from domain.exceptions.project_management import ProjectSubmissionAlreadyProcessedException
from domain.models.project_management.project import Project
from domain.models.user import User
from domain.ports.service import AbstractDomainService
from domain.repositories.project.project import ProjectWriteRepository
from domain.services.permission import PermissionService
from domain.value_objects.common import Id
from domain.value_objects.project.project import ProjectUpdatePayload
from loguru import logger


class ProjectSubmissionPermissionService(AbstractDomainService):
    def __init__(
        self,
        permisison_service: PermissionService,
    ):
        self._permission_service = permisison_service

    def _check_permission_to_change_project_status(self, user: User) -> None:
        """:raises UpdateDeniedPermissionException:"""

        change_any_project_status_permission = self._permission_service.create_permission_vo(
            model=Project, action=ActionEnum.CHANGE, scope=ScopeEnum.ANY, field=Project.STATUS_FIELD
        )
        has_permission = self._permission_service.has_user_permission(
            user=user, permission_vo=change_any_project_status_permission
        )
        if has_permission:
            logger.debug("User has enough permissions to change project status.")
            return None

        logger.error(f"User(id={user.id}) doesn't have enough permissions to change a project status.")
        raise UpdateDeniedPermissionException("You don't have enough permissions to change project status.")


class ProjectSubmissionService(ProjectSubmissionPermissionService):
    def __init__(
        self,
        permisison_service: PermissionService,
        project_write_repository: ProjectWriteRepository,
    ):
        super().__init__(permisison_service=permisison_service)
        self._project_write_repository = project_write_repository

    def approve(self, user: User, project: Project) -> None:
        self._check_submission_not_processed(project=project)
        self._check_permission_to_change_project_status(user=user)

        approve_payload = ProjectUpdatePayload(id_=Id(value=project.id), status=ProjectStatusEnum.ACTIVE)
        self._project_write_repository.update(data=approve_payload)
        logger.info(f"Project(id={project.id}) has approved successfully.")

    def reject(self, user: User, project: Project) -> None:
        self._check_submission_not_processed(project=project)
        self._check_permission_to_change_project_status(user=user)

        reject_payload = ProjectUpdatePayload(id_=Id(value=project.id), status=ProjectStatusEnum.REJECTED)
        self._project_write_repository.update(data=reject_payload)
        logger.info(f"Project(id={project.id}) has rejected successfully.")

    def _check_submission_not_processed(self, project: Project) -> None:
        """:raises ProjectSubmissionAlreadyProcessedException:"""
        if project.status != ProjectStatusEnum.UNDER_MODERATION:
            raise ProjectSubmissionAlreadyProcessedException("This project's submission already processed.")
