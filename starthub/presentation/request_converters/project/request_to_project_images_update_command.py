from typing import Any

from domain.value_objects.common import Id, Order
from domain.value_objects.project.image import ProjectImageUpdateCommand
from loguru import logger
from presentation.request_converters.common import get_required_field


def request_project_data_to_project_images_update_command(
    data: dict[str, Any], project_id: int, user_id: int
) -> ProjectImageUpdateCommand:
    new_order: list[Order] = list()

    for i in get_required_field(data, "new_order"):
        logger.debug(f"i = {repr(i)}")
        new_order.append(Order(value=i))
    logger.debug(f"{new_order=}")
    return ProjectImageUpdateCommand(project_id=Id(value=project_id), user_id=Id(value=user_id), new_order=new_order)
