from domain.constants import PROJECT_REJECTED_REPORT_MAX_LENGTH
from domain.ports.command import BaseCommand
from domain.value_objects.common import StringVo


class ProjectRejectReport(StringVo):
    max_length = PROJECT_REJECTED_REPORT_MAX_LENGTH


class ProjectRejectCommand(BaseCommand):
    report: ProjectRejectReport
