import json
from typing import Any, cast

from django.core.files.uploadedfile import UploadedFile
from django.utils.datastructures import MultiValueDict
from domain.value_objects.common import DeadlineDate, Description, FirstName, Id, LastName, Order
from domain.value_objects.company import CompanyFounderCreateCommand
from domain.value_objects.file import ImageFile, PdfFile
from domain.value_objects.project_management import (
    GoalSum,
    ProjectImageCreateCommand,
    ProjectImageUpdateCommand,
    ProjectName,
    ProjectStage,
    ProjectUpdateCommand,
    TeamMemberCreateCommand,
)
from loguru import logger
from presentation.request_converters.common import get_required_field, parse_date
from rest_framework.request import Request


def _request_data_to_team_members(data: dict[str, str]) -> list[TeamMemberCreateCommand]:
    """
    :raises MissingRequiredFieldException:
    :raises FirstNameIsTooLongException:
    :raises LastNameIsTooLongException:
    :raises EmptyStringException:
    """
    logger.debug("Started _request_data_to_team_members()")

    team_members_data = json.loads(get_required_field(data, field="team_members"))

    logger.debug(f"team_members = {team_members_data}")
    team_members: list[TeamMemberCreateCommand] = []

    for member in team_members_data:
        team_members.append(
            TeamMemberCreateCommand(
                first_name=FirstName(value=get_required_field(member, field="first_name")),
                last_name=LastName(value=get_required_field(member, field="last_name")),
                description=Description(value=member["description"]),
            )
        )
    return team_members


def _request_data_to_company_founder_create_command(data: dict[str, Any]) -> CompanyFounderCreateCommand:
    founder_data: dict[str, Any] = json.loads(get_required_field(data, field="company_founder"))
    return CompanyFounderCreateCommand(
        name=FirstName(value=get_required_field(founder_data, "first_name", "founder_first_name")),
        surname=LastName(value=get_required_field(founder_data, "last_name", "founder_last_name")),
        description=Description(value=get_required_field(founder_data, "description", "founder_description")),
    )


def _request_files_to_project_plan(files: MultiValueDict[str, UploadedFile]) -> PdfFile:
    project_plan_file: UploadedFile = get_required_field(cast(dict[str, UploadedFile], files), field="project_plan")
    logger.debug(f"{project_plan_file=}")
    project_plan_file.seek(0)
    pdf_file = PdfFile(value=project_plan_file.read())
    logger.debug(f"{pdf_file=}")
    return pdf_file


########################################################################################################################
# Project Update Converter
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

    return ProjectUpdateCommand(
        project_id=Id(value=project_id),
        user_id=Id(value=user_id),
        name=ProjectName(value=project_data["name"]) if "name" in project_data else None,
        category_ids=category_ids,
        funding_model_id=Id(value=project_data["funding_model_id"]) if "funding_model_id" in project_data else None,
        stage=ProjectStage(value=project_data["stage"]) if "stage" in project_data else None,
        goal_sum=GoalSum(value=project_data["goal_sum"]) if "goal_sum" in project_data else None,
        deadline=DeadlineDate(value=parse_date(project_data["deadline"])) if "deadline" in project_data else None,
        plan_file=project_plan,
    )


########################################################################################################################
# Project Image Converter
def request_files_to_project_image_create_command(
    files: dict[str, UploadedFile],
    project_id: int,
    user_id: int,
) -> ProjectImageCreateCommand:
    project_image_file: UploadedFile = get_required_field(files, "project_image")
    project_image_file.seek(0)
    image = ImageFile(value=project_image_file.read())
    logger.debug("request.FILES -> ImageFile conversion OK")
    project_image_create = ProjectImageCreateCommand(
        user_id=Id(value=user_id), project_id=Id(value=project_id), image_file=image
    )
    logger.debug("ProjectImageCreateCommand converted")
    return project_image_create


def request_project_data_to_project_images_update_command(
    data: dict[str, Any], project_id: int, user_id: int
) -> ProjectImageUpdateCommand:
    new_order: list[Order] = list()

    for i in get_required_field(data, "new_order"):
        logger.debug(f"i = {repr(i)}")
        new_order.append(Order(value=i))
    logger.debug(f"{new_order=}")
    return ProjectImageUpdateCommand(project_id=Id(value=project_id), user_id=Id(value=user_id), new_order=new_order)
