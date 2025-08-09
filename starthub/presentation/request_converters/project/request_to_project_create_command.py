import json
from pprint import pformat
from typing import Any, cast

from django.core.files.uploadedfile import UploadedFile
from django.utils.datastructures import MultiValueDict
from domain.value_objects.common import DeadlineDate, Description, FirstName, Id, LastName, PhoneNumber, SocialLink
from domain.value_objects.company import (
    BusinessNumber,
    CompanyFounderCreateCommand,
    CompanyName,
    EstablishedDate,
    PatentNumber,
)
from domain.value_objects.country import CountryCode
from domain.value_objects.file import ImageFile, PdfFile
from domain.value_objects.project.accelerator import AcceleratorName, ProjectAcceleratorCreateCommand
from domain.value_objects.project.common import GoalSum, ProjectName, ProjectStage
from domain.value_objects.project.incubator import IncubatorCreateCommand, IncubatorName
from domain.value_objects.project.project import ProjectCreateCommand
from domain.value_objects.project.team_member import TeamMemberCreateCommand
from loguru import logger
from presentation.request_converters.common import build_address_create_command, get_required_field, parse_date
from presentation.request_converters.project.common import extract_steps
from rest_framework.request import Request


def request_to_project_create_command(request: Request, user_id: int) -> ProjectCreateCommand:
    """
    Convert Django request to ProjectCreateCommand.

    :param request: Django REST framework request
    :param user_id: ID of the user creating the project
    :return: ProjectCreateCommand instance
    :raises InvalidPhoneNumberException:
    :raises NegativeProjectGoalSumException:
    :raises ProjectDeadlineInPastValidationException:
    :raises DateIsNotIsoFormatException:
    :raises DisallowedSocialLinkException:
    :raises InvalidProjectStageException:
    :raises InvalidSocialLinkException:
    :raises MissingRequiredFieldException:
    :raises FirstNameIsTooLongException:
    :raises LastNameIsTooLongException:
    :raises EmptyStringException:
    :raises ValidationError: when a field has incorrect type.
    :raises DateInFutureException:
    :raises NotPdfFileException:
    """
    data = request.data
    files = request.FILES

    # Parse JSON data from request
    project_data = _parse_json_field(data, "project")
    company_data = _parse_json_field(data, "company")

    # Extract core project data
    project_info = _extract_project_info(project_data, user_id)
    company_info = _extract_company_info(company_data)

    # Process files
    project_plan = _extract_project_plan(files)
    project_images = _extract_project_images(files)

    # Process related entities
    team_members = _extract_team_members(data)
    company_founder = _extract_company_founder(data)

    incubator: IncubatorCreateCommand | None = None
    if "incubator" in data:
        incubator = _extract_incubator(raw_data=data)

    accelerator: ProjectAcceleratorCreateCommand | None = None
    if "accelerator" in data:
        accelerator = _extract_accelerator(raw_data=data)

    command = ProjectCreateCommand(
        **project_info,
        **company_info,
        plan_file=project_plan,
        images=project_images,
        team_members=team_members,
        company_founder=company_founder,
        incubator=incubator,
        accelerator=accelerator,
    )

    logger.debug(f"command: \n{pformat(command.__dict__)}")
    return command


def _parse_json_field(data: dict[str, Any], field_name: str) -> Any:
    """Parse JSON field from request data."""
    return json.loads(get_required_field(data, field=field_name))


def _extract_project_info(project_data: dict[str, Any], user_id: int) -> dict[str, Any]:
    """Extract project-specific information from request data."""
    return {
        "name": ProjectName(value=get_required_field(project_data, field="name")),
        "creator_id": Id(value=user_id),
        "goal_description": (
            Description(value=project_data["goal_description"]) if "goal_description" in project_data else None
        ),
        "description": Description(value=get_required_field(project_data, field="description")),
        "category_ids": [Id(value=i) for i in get_required_field(project_data, "category_ids")],
        "funding_model_id": Id(value=get_required_field(project_data, field="funding_model_id")),
        "stage": ProjectStage(value=get_required_field(project_data, field="stage")),
        "goal_sum": GoalSum(value=get_required_field(project_data, field="goal_sum")),
        "deadline": DeadlineDate(value=parse_date(get_required_field(project_data, field="deadline"))),
        "social_links": [
            SocialLink(platform=k, link=v) for k, v in get_required_field(project_data, "social_links").items()
        ],
        "steps": extract_steps(project_data),
        "phone_number": PhoneNumber(value=get_required_field(project_data, "phone_number")),
    }


def _extract_accelerator(raw_data: dict[str, str]) -> ProjectAcceleratorCreateCommand:
    accelerator_data = _parse_json_field(raw_data, "accelerator")
    logger.debug(f"accelerator_data = {accelerator_data}")

    accelerator = ProjectAcceleratorCreateCommand(
        name=AcceleratorName(value=get_required_field(accelerator_data, "name")),
        description=Description(value=get_required_field(accelerator_data, "description")),
    )
    return accelerator


def _extract_incubator(raw_data: dict[str, str]) -> IncubatorCreateCommand:
    incubator_data = _parse_json_field(raw_data, "incubator")
    logger.debug(f"incubator_data = {incubator_data}")

    incubator = IncubatorCreateCommand(
        name=IncubatorName(value=get_required_field(incubator_data, "name", "incubator.name")),
        description=Description(value=get_required_field(incubator_data, "description", "incubator.description")),
    )
    return incubator


def _extract_company_info(company_data: dict[str, Any]) -> dict[str, Any]:
    """Extract company-specific information from request data."""
    country_code = CountryCode(value=get_required_field(company_data, "country_code", "company.country_code"))
    address_create_command = build_address_create_command(
        get_required_field(company_data, "address", "company.address")
    )
    patent_number: PatentNumber | None = None
    if "patent_number" in company_data:
        if company_data["patent_number"] is not None:
            patent_number = PatentNumber(value=company_data["patent_number"])

    return {
        "company_name": CompanyName(value=get_required_field(company_data, "name", "company.name")),
        "country_code": country_code,
        "company_address": address_create_command,
        "business_id": BusinessNumber(
            value=get_required_field(company_data, "business_id", "company.business_id"), country_code=country_code
        ),
        "established_date": EstablishedDate(
            value=parse_date(get_required_field(company_data, "established_date", "company.established_date"))
        ),
        "patent_number": patent_number,
    }


def _extract_project_plan(files: MultiValueDict[str, UploadedFile]) -> PdfFile:
    """Extract and convert project plan file to PdfFile."""
    project_plan_file: UploadedFile = get_required_field(cast(dict[str, UploadedFile], files), field="project_plan")

    logger.debug(f"{project_plan_file=}")
    project_plan_file.seek(0)
    pdf_file = PdfFile(value=project_plan_file.read())
    logger.debug(f"{pdf_file=}")

    return pdf_file


def _extract_project_images(files: MultiValueDict[str, UploadedFile]) -> list[ImageFile]:
    """Extract and convert project images to ImageFile list."""
    project_images: list[ImageFile] = []
    images: list[UploadedFile] = files.getlist("images")

    for image in images:
        image.seek(0)
        project_images.append(ImageFile(value=image.read()))

    logger.debug("request.FILES -> ImageFile conversion OK")
    return project_images


def _extract_team_members(data: dict[str, str]) -> list[TeamMemberCreateCommand]:
    """
    Extract team members from request data.

    :raises MissingRequiredFieldException:
    :raises FirstNameIsTooLongException:
    :raises LastNameIsTooLongException:
    :raises EmptyStringException:
    """
    logger.debug("Started _request_data_to_team_members()")

    team_members_data: list[dict[str, Any]] = _parse_json_field(data, "team_members")
    logger.debug(f"team_members = {team_members_data}")

    team_members: list[TeamMemberCreateCommand] = []
    for member in team_members_data:
        team_member = TeamMemberCreateCommand(
            first_name=FirstName(value=get_required_field(member, field="first_name")),
            last_name=LastName(value=get_required_field(member, field="last_name")),
            description=Description(value=get_required_field(member, field="description")),
        )
        team_members.append(team_member)

    return team_members


def _extract_company_founder(data: dict[str, Any]) -> CompanyFounderCreateCommand:
    """Extract company founder information from request data."""
    founder_data = _parse_json_field(data, "company_founder")

    return CompanyFounderCreateCommand(
        name=FirstName(value=get_required_field(founder_data, "first_name", "founder_first_name")),
        surname=LastName(value=get_required_field(founder_data, "last_name", "founder_last_name")),
        description=Description(value=get_required_field(founder_data, "description", "founder_description")),
    )
