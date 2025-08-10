import json
from typing import Any

from django.core.files.uploadedfile import UploadedFile
from domain.value_objects.common import DeadlineDate, Description, Id
from domain.value_objects.file import PdfFile
from domain.value_objects.project.accelerator import AcceleratorName, ProjectAcceleratorUpdatePayload
from domain.value_objects.project.common import GoalSum, ProjectName, ProjectStage
from domain.value_objects.project.incubator import IncubatorName, IncubatorUpdatePayload
from domain.value_objects.project.project import ProjectUpdateCommand
from loguru import logger
from presentation.request_converters.common import parse_date
from presentation.request_converters.project.common import extract_steps
from rest_framework.request import Request


def request_to_the_project_update_command(request: Request, project_id: int, user_id: int) -> ProjectUpdateCommand:
    data = request.data
    files = request.FILES

    logger.debug(f"{data=}")

    project_data: dict[str, Any] = dict()
    if "project" in data:
        project_data = json.loads(data["project"])
        logger.debug(f"{project_data=}")

    category_ids: list[Id] | None = None
    if "category_ids" in project_data:
        logger.debug(f"{project_data.get("category_ids")=}")
        category_ids = [Id(value=i) for i in project_data["category_ids"]]

    project_plan: PdfFile | None = None
    if "project_plan" in files:
        project_plan_file: UploadedFile = files["project_plan"]
        project_plan_file.seek(0)
        project_plan = PdfFile(value=project_plan_file.read())

    description: Description | None = (
        Description(value=project_data["description"]) if "description" in project_data else None
    )
    goal_description: Description | None = (
        Description(value=project_data["goal_description"]) if "goal_description" in project_data else None
    )
    incubator: IncubatorUpdatePayload | None = None
    if "incubator" in project_data:
        incubator_info = project_data["incubator"]
        incubator = IncubatorUpdatePayload(
            project_id=Id(value=project_id),
            name=IncubatorName(value=incubator_info["name"]) if "name" in incubator_info else None,
            description=Description(value=incubator_info["description"]) if "description" in incubator_info else None,
        )
    accelerator: ProjectAcceleratorUpdatePayload | None = None
    if "accelerator" in project_data:
        accelerator_info = project_data["accelerator"]
        accelerator = ProjectAcceleratorUpdatePayload(
            project_id=Id(value=project_id),
            name=AcceleratorName(value=accelerator_info["name"]),
            description=Description(value=accelerator_info["description"]),
        )
    return ProjectUpdateCommand(
        project_id=Id(value=project_id),
        user_id=Id(value=user_id),
        name=ProjectName(value=project_data["name"]) if "name" in project_data else None,
        description=description,
        goal_description=goal_description,
        category_ids=category_ids,
        funding_model_id=Id(value=project_data["funding_model_id"]) if "funding_model_id" in project_data else None,
        stage=ProjectStage(value=project_data["stage"]) if "stage" in project_data else None,
        steps=extract_steps(project_data) if "project_steps" in project_data else None,
        goal_sum=GoalSum(value=project_data["goal_sum"]) if "goal_sum" in project_data else None,
        deadline=DeadlineDate(value=parse_date(project_data["deadline"])) if "deadline" in project_data else None,
        plan_file=project_plan,
        incubator=incubator,
        accelerator=accelerator,
    )
