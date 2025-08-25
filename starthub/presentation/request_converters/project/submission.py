from domain.value_objects.project.report import ProjectReportContent
from domain.value_objects.project.submission import ProjectRejectCommand
from presentation.request_converters.common import get_required_field
from rest_framework.request import Request


def request_to_project_submission_reject_command(request: Request) -> ProjectRejectCommand:
    data = request.data
    return ProjectRejectCommand(report=ProjectReportContent(value=get_required_field(data, "report")))
