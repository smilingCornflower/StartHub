from pprint import pformat
from typing import Any

from domain.value_objects.common import SocialLink
from domain.value_objects.project.investment import (
    ProjectInvestmentAmount,
    ProjectInvestmentCreateCommand,
    ProjectInvestmentOrganizationName,
)
from loguru import logger
from presentation.request_converters.common import get_required_field
from rest_framework.request import Request


def request_to_project_investment_create_command(request: Request) -> ProjectInvestmentCreateCommand:
    data: dict[str, Any] = request.data

    command = ProjectInvestmentCreateCommand(
        organization_name=ProjectInvestmentOrganizationName(value=get_required_field(data, "organization_name")),
        amount=ProjectInvestmentAmount(value=float(get_required_field(data, "amount"))),
        social_links=[SocialLink(platform=k, link=v) for k, v in get_required_field(data, "social_links").items()],
    )
    logger.debug(f"command: \n {pformat(command.__dict__)}")
    return command
