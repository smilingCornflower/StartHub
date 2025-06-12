import json
from datetime import date
from typing import Any, cast

from application.converters.request_converters.common import get_required_field, parse_date
from django.core.files.uploadedfile import UploadedFile
from django.http import QueryDict
from domain.value_objects.common import FirstName, Id, LastName, PhoneNumber, Slug, SocialLink
from domain.value_objects.company import BusinessNumber, CompanyCreateCommand, CompanyFounderCreatePayload
from domain.value_objects.country import CountryCode
from domain.value_objects.file import PdfFile
from domain.value_objects.filter import ProjectFilter
from domain.value_objects.project_management import ProjectCreateCommand, ProjectStage, TeamMemberCreateCommand
from loguru import logger


def request_data_to_project_filter(data: QueryDict) -> ProjectFilter:

    filter_ = ProjectFilter()

    if data.get("category_slug"):
        filter_.category_slug = Slug(value=cast(str, data.get("category_slug")))
    if data.get("funding_model_slug"):
        filter_.funding_model_slug = Slug(value=cast(str, data.get("funding_model_slug")))

    return filter_


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
                description=member["description"],
            )
        )
    return team_members


def _request_data_to_company_create_command(data: dict[str, Any], user_id: int) -> CompanyCreateCommand:
    logger.debug("Started _request_data_to_company_create_command()")
    company_data: dict[str, Any] = json.loads(get_required_field(data, field="company"))
    founder_data: dict[str, Any] = json.loads(get_required_field(data, field="company_founder"))

    established_date: date = parse_date(get_required_field(company_data, "established_date"))

    founder_create_command = CompanyFounderCreatePayload(
        name=FirstName(value=get_required_field(founder_data, "first_name")),
        surname=LastName(value=get_required_field(founder_data, "last_name")),
        description=founder_data.get("description"),
    )
    country_code = CountryCode(value=get_required_field(company_data, "country_code"))

    return CompanyCreateCommand(
        name=get_required_field(company_data, "name"),
        description=get_required_field(company_data, "description"),
        representative_id=Id(value=user_id),
        country_code=country_code,
        business_id=BusinessNumber(value=get_required_field(company_data, "business_id"), country_code=country_code),
        established_date=established_date,
        founder_create_payload=founder_create_command,
    )


def request_data_to_project_create_command(
    data: dict[str, str], files: dict[str, UploadedFile], user_id: int
) -> ProjectCreateCommand:
    """
    :raises InvalidPhoneNumberException:
    :raises NegativeProjectGoalSumValidationException:
    :raises ProjectDeadlineInPastValidationException:
    :raises DateIsNotIsoFormatException:
    :raises InvalidPhoneNumberException:
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
    project_data = json.loads(get_required_field(data, field="project"))
    project_plan_file: UploadedFile = cast(UploadedFile, get_required_field(files, field="project_plan"))
    project_plan_file.seek(0)
    project_plan_data = PdfFile(value=project_plan_file.read())

    return ProjectCreateCommand(
        name=get_required_field(project_data, field="name"),
        creator_id=Id(value=user_id),
        description=get_required_field(project_data, field="description"),
        category_id=Id(value=get_required_field(project_data, field="category_id")),
        funding_model_id=Id(value=get_required_field(project_data, field="funding_model_id")),
        stage=ProjectStage(value=get_required_field(project_data, field="stage")),
        goal_sum=get_required_field(project_data, field="goal_sum"),
        deadline=parse_date(get_required_field(project_data, field="deadline")),
        team_members=_request_data_to_team_members(data),
        company=_request_data_to_company_create_command(data, user_id),
        social_links=[
            SocialLink(platform=k, link=v) for k, v in get_required_field(project_data, "social_links").items()
        ],
        phone_number=PhoneNumber(value=get_required_field(project_data, "phone_number")),
        project_plan_data=project_plan_data,
    )
