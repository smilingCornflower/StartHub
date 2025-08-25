from domain.events.project import ProjectRejectedEvent
from domain.ports.event import AbstractEventHandler
from domain.services.project_management.report import ProjectReportService
from domain.value_objects.project.report import ProjectReportCreatePayload


class ProjectRejectedReportEventHandler(AbstractEventHandler[ProjectRejectedEvent]):
    def __init__(self, project_report_service: ProjectReportService):
        self._project_report_service = project_report_service

    def handle(self, event: ProjectRejectedEvent) -> None:
        report_create_payload = ProjectReportCreatePayload(project_id=event.project_id, content=event.report)
        self._project_report_service.create(payload=report_create_payload)
