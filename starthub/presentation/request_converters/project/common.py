from typing import Any

from domain.value_objects.common import Description
from domain.value_objects.project.step import ProjectStepCreateCommand, ProjectStepDate, ProjectStepName
from presentation.request_converters.common import get_required_field, parse_date


def extract_steps(data: dict[str, Any]) -> list[ProjectStepCreateCommand]:
    project_steps = get_required_field(data, "project_steps")

    result: list[ProjectStepCreateCommand] = list()
    for step in project_steps:
        name = ProjectStepName(value=get_required_field(step, "name", "project_steps.name"))
        description = Description(value=get_required_field(step, "description", "project_steps.description"))
        step_date = ProjectStepDate(value=parse_date(get_required_field(step, "date", "project_steps.date")))
        result.append(ProjectStepCreateCommand(name=name, description=description, date=step_date))

    return result
