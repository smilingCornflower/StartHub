from domain.ports.command import BaseCommand
from domain.value_objects.common import DeadlineDate, Description, MediumString


class ProjectStepName(MediumString):
    pass


class ProjectStepDate(DeadlineDate):
    pass


class ProjectStepCreateCommand(BaseCommand):
    name: ProjectStepName
    description: Description
    date: ProjectStepDate
