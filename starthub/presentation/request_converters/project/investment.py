from pprint import pformat
from typing import Any

from loguru import logger
from rest_framework.request import Request

from domain.value_objects.common import PhoneNumber, SocialLink
from domain.value_objects.project.investment import (
    ProjectInvestmentAmount,
    ProjectInvestmentCreateCommand,
    ProjectInvestmentOrganizationName,
    ProjectInvestmentUpdateCommand,
)
from presentation.request_converters.common import get_required_field


def request_to_project_investment_create_command(request: Request) -> ProjectInvestmentCreateCommand:
    data: dict[str, Any] = request.data

    command = ProjectInvestmentCreateCommand(
        organization_name=ProjectInvestmentOrganizationName(value=get_required_field(data, "organization_name")),
        amount=ProjectInvestmentAmount(value=float(get_required_field(data, "amount"))),
        social_links=[SocialLink(platform=k, link=v) for k, v in get_required_field(data, "social_links").items()],
        phone_numbers=[PhoneNumber(value=i) for i in get_required_field(data, "phone_numbers")],
    )
    logger.debug(f"command: \n {pformat(command.__dict__)}")
    return command


def request_to_project_investment_update_command(request: Request) -> ProjectInvestmentUpdateCommand:
    data: dict[str, Any] = request.data

    command = ProjectInvestmentUpdateCommand(
        organization_name=(
            ProjectInvestmentOrganizationName(value=data["organization_name"]) if "organization_name" in data else None
        ),
        amount=ProjectInvestmentAmount(value=float(data["amount"])) if "amount" in data else None,
        social_links=(
            [SocialLink(platform=k, link=v) for k, v in data["social_links"].items()]
            if "social_links" in data
            else None
        ),
    )
    logger.debug(f"command: \n {pformat(command.__dict__)}")
    return command


def request_to_social_link(request: Request) -> list[SocialLink]:
    data: dict[str, Any] = request.data
    social_link = [SocialLink(platform=k, link=v) for k, v in get_required_field(data, "social_links").items()]

    logger.debug(f"social_links = {social_link}")
    return social_link


def request_to_phone(request: Request) -> PhoneNumber:
    data = request.data
    project_phone = PhoneNumber(value=get_required_field(data, "phone_number"))
    return project_phone
