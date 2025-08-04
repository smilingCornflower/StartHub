import json
from pprint import pformat
from typing import Any, cast

from django.core.files.uploadedfile import UploadedFile
from django.utils.datastructures import MultiValueDict
from domain.value_objects.common import (
    CountryCode,
    DeadlineDate,
    Description,
    FirstName,
    Id,
    LastName,
    PhoneNumber,
    SocialLink,
)
from domain.value_objects.company import BusinessNumber, CompanyFounderCreateCommand, CompanyName, EstablishedDate
from domain.value_objects.file import ImageFile, PdfFile
from domain.value_objects.geo import AddressCreateCommand
from domain.value_objects.project_management import (
    GoalSum,
    ProjectCreateCommand,
    ProjectName,
    ProjectStage,
    TeamMemberCreateCommand,
)
from loguru import logger
from presentation.request_converters.common import get_required_field, parse_date
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

    command = ProjectCreateCommand(
        **project_info,
        **company_info,
        plan_file=project_plan,
        images=project_images,
        team_members=team_members,
        company_founder=company_founder,
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
        "description": Description(value=get_required_field(project_data, field="description")),
        "category_ids": [Id(value=i) for i in get_required_field(project_data, "category_ids")],
        "funding_model_id": Id(value=get_required_field(project_data, field="funding_model_id")),
        "stage": ProjectStage(value=get_required_field(project_data, field="stage")),
        "goal_sum": GoalSum(value=get_required_field(project_data, field="goal_sum")),
        "deadline": DeadlineDate(value=parse_date(get_required_field(project_data, field="deadline"))),
        "social_links": [
            SocialLink(platform=k, link=v) for k, v in get_required_field(project_data, "social_links").items()
        ],
        "phone_number": PhoneNumber(value=get_required_field(project_data, "phone_number")),
    }


def _extract_company_info(company_data: dict[str, Any]) -> dict[str, Any]:
    """Extract company-specific information from request data."""
    country_code = CountryCode(value=get_required_field(company_data, "country_code", "company.country_code"))
    address_create_command = _build_address_create_command(
        get_required_field(company_data, "address", "company.address"), country_code
    )

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
    }


def _build_address_create_command(address_data: dict[str, str], country_code: CountryCode) -> AddressCreateCommand:
    """Build AddressVo from address data."""
    return AddressCreateCommand(
        country_code=country_code,
        region_id=Id(value=int(get_required_field(address_data, "region_id"))),
        city_id=Id(value=int(get_required_field(address_data, "city_id"))),
        district=address_data.get("district"),
        street=address_data.get("street"),
        house_number=address_data.get("house_number"),
        postal_code=address_data.get("postal_code"),
        raw_address=address_data.get("raw_address"),
    )


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
