from domain.value_objects.project.funding_model import FundingModelUpdateCommand
from loguru import logger
from rest_framework.request import Request


def request_to_funding_model_update_command(request: Request) -> FundingModelUpdateCommand:
    data = request.data

    command = FundingModelUpdateCommand(
        name=data.get("name"),
        description=data.get("description"),
        recommended=data.get("recommended"),
    )
    logger.debug(f"command = {command}")
    return command
