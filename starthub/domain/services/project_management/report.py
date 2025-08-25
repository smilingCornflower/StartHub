from domain.exceptions.permissions import ViewDeniedPermissionException
from domain.models.project_management.project import Project
from domain.models.user_management.user import User
from domain.ports.service import AbstractDomainService
from domain.repositories.project.report import ProjectReportWriteRepository
from domain.services.permission import PermissionService
from domain.value_objects.project.report import ProjectReportCreatePayload
from loguru import logger


class ProjectReportPermissionService(AbstractDomainService):
    def __init__(self, permission_service: PermissionService):
        self._permission_service = permission_service

    def check_can_user_read_reports_for_project(self, user: User, project: Project) -> None:
        """:raises ViewDeniedPermissionException:"""
        if user == project.creator:
            return None
        else:
            raise ViewDeniedPermissionException("You don't have enough permissions to read reports for this project.")


class ProjectReportService(ProjectReportPermissionService):
    def __init__(
        self,
        permission_service: PermissionService,
        write_repository: ProjectReportWriteRepository,
    ):
        super().__init__(permission_service=permission_service)
        self._write_repository = write_repository

    def create(self, payload: ProjectReportCreatePayload) -> None:
        self._write_repository.create(data=payload)
        logger.info("Project report created successfully.")
