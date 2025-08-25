from domain.ports.command import BaseCommand
from domain.value_objects.project.report import ProjectReportContent


class ProjectRejectCommand(BaseCommand):
    report: ProjectReportContent
