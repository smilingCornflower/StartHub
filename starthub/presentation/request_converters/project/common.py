from typing import Any

from domain.value_objects.common import Description, PhoneNumber, SocialLink
from domain.value_objects.project.step import ProjectStepCreateCommand, ProjectStepDate, ProjectStepName
from loguru import logger
from presentation.request_converters.common import get_required_field, parse_date
from rest_framework.request import Request


def extract_steps(data: dict[str, Any]) -> list[ProjectStepCreateCommand]:
    project_steps = get_required_field(data, "project_steps")

    result: list[ProjectStepCreateCommand] = list()
    for step in project_steps:
        name = ProjectStepName(value=get_required_field(step, "name", "project_steps.name"))
        description = Description(value=get_required_field(step, "description", "project_steps.description"))
        step_date = ProjectStepDate(value=parse_date(get_required_field(step, "date", "project_steps.date")))
        result.append(ProjectStepCreateCommand(name=name, description=description, date=step_date))

    return result


def request_to_social_link(request: Request) -> list[SocialLink]:
    data: dict[str, Any] = request.data
    social_link = [SocialLink(platform=k, link=v) for k, v in get_required_field(data, "social_links").items()]

    logger.debug(f"social_links = {social_link}")
    return social_link


def request_to_phone(request: Request) -> PhoneNumber:
    data = request.data
    project_phone = PhoneNumber(value=get_required_field(data, "phone_number"))
    return project_phone
