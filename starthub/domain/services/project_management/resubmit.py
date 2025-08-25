from domain.enums.project_status import ProjectStatusEnum
from domain.exceptions.permissions import ViewDeniedPermissionException
from domain.exceptions.project_management import ProjectResubmitException
from domain.models.project_management.project import Project
from domain.models.user_management.user import User
from domain.ports.service import AbstractDomainService
from domain.repositories.project.project import ProjectWriteRepository
from domain.services.project_management.project import ProjectService
from domain.value_objects.common import Id
from domain.value_objects.project.project import ProjectUpdatePayload
from loguru import logger


class ProjectResubmitService(AbstractDomainService):
    def __init__(self, project_service: ProjectService, write_repository: ProjectWriteRepository):
        self._project_service = project_service
        self._write_repository = write_repository

    def resubmit(self, user: User, project: Project) -> None:
        self.check_can_user_resubmit(user=user, project=project)
        self.check_project_can_be_resubmitted(project=project)

        resubmit_payload = ProjectUpdatePayload(
            id_=Id(value=project.id),
            status=ProjectStatusEnum.UNDER_MODERATION,
        )
        self._write_repository.update(data=resubmit_payload)
        logger.info("Project was sent to moderation.")

    def check_can_user_resubmit(self, user: User, project: Project) -> None:
        """:raises ViewDeniedPermissionException:"""
        if user == project.creator:
            return None
        raise ViewDeniedPermissionException("You don't have enough permissions to resubmit this project.")

    def check_project_can_be_resubmitted(self, project: Project) -> None:
        """:raises ProjectResubmitException:"""
        if project.status == ProjectStatusEnum.REJECTED:
            return None
        else:
            raise ProjectResubmitException("Project must have 'rejected' status to be resubmitted.")
