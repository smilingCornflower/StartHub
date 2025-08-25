from domain.ports.service import AbstractDomainService
from domain.repositories.project.report import ProjectReportWriteRepository
from domain.services.permission import PermissionService
from domain.value_objects.project.report import ProjectReportCreatePayload
from loguru import logger


class ProjectReportPermissionService(AbstractDomainService):
    def __init__(self, permission_service: PermissionService):
        self._permission_service = permission_service


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
