import json
from typing import Any, cast

from application.converters.request_converters.common import get_required_field, parse_date
from django.core.files.uploadedfile import UploadedFile
from django.http import QueryDict
from domain.value_objects.common import (
    DeadlineDate,
    Description,
    FirstName,
    Id,
    LastName,
    PhoneNumber,
    Slug,
    SocialLink,
)
from domain.value_objects.company import (
    BusinessNumber,
    CompanyFounderCreateCommand,
    CompanyName,
    CompanyUpdatePayload,
    EstablishedDate,
)
from domain.value_objects.country import CountryCode
from domain.value_objects.file import PdfFile
from domain.value_objects.filter import ProjectFilter
from domain.value_objects.project_management import (
    GoalSum,
    ProjectCreateCommand,
    ProjectName,
    ProjectStage,
    ProjectUpdateCommand,
    TeamMemberCreateCommand,
)
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


def _request_files_to_project_plan(files: dict[str, UploadedFile]) -> PdfFile:
    project_plan_file: UploadedFile = cast(UploadedFile, get_required_field(files, field="project_plan"))
    project_plan_file.seek(0)
    return PdfFile(value=project_plan_file.read())


def request_data_to_project_create_command(
    data: dict[str, str], files: dict[str, UploadedFile], user_id: int
) -> ProjectCreateCommand:
    """
    :raises InvalidPhoneNumberException:
    :raises NegativeProjectGoalSumException:
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
    company_data = json.loads(get_required_field(data, field="company"))
    project_plan: PdfFile = _request_files_to_project_plan(files=files)
    country_code = CountryCode(value=get_required_field(company_data, "country_code", "company.country_code"))
    return ProjectCreateCommand(
        name=ProjectName(value=get_required_field(project_data, field="name")),
        creator_id=Id(value=user_id),
        description=Description(value=get_required_field(project_data, field="description")),
        category_id=Id(value=get_required_field(project_data, field="category_id")),
        funding_model_id=Id(value=get_required_field(project_data, field="funding_model_id")),
        stage=ProjectStage(value=get_required_field(project_data, field="stage")),
        goal_sum=GoalSum(value=get_required_field(project_data, field="goal_sum")),
        deadline=DeadlineDate(value=parse_date(get_required_field(project_data, field="deadline"))),
        social_links=[
            SocialLink(platform=k, link=v) for k, v in get_required_field(project_data, "social_links").items()
        ],
        phone_number=PhoneNumber(value=get_required_field(project_data, "phone_number")),
        plan_file=project_plan,
        company_name=CompanyName(value=get_required_field(company_data, "name", "company.name")),
        country_code=country_code,
        business_id=BusinessNumber(
            value=get_required_field(company_data, "business_id", "company.business_id"), country_code=country_code
        ),
        established_date=EstablishedDate(
            value=parse_date(get_required_field(company_data, "established_date", "company.established_date"))
        ),
        team_members=_request_data_to_team_members(data),
        company_founder=_request_data_to_company_founder_create_command(data=data),
    )


########################################################################################################################
# Project Update Converter
def request_data_to_the_project_update_command(
    data: dict[str, str], files: dict[str, UploadedFile], project_id: int, user_id: int
) -> ProjectUpdateCommand:
    logger.debug(f"{data=}")

    project_data: dict[str, Any] = dict()
    if "project" in data:
        project_data = json.loads(data["project"])
        logger.debug(f"{project_data=}")

    company_update_command: CompanyUpdatePayload | None = None
    if "company" in data:
        company_data = json.loads(data["company"])
        logger.debug(f"{company_data=}")
        company_update_command = CompanyUpdatePayload(
            project_id=Id(value=project_id),
            name=CompanyName(value=company_data["name"]) if "name" in company_data else None,
            description=Description(value=company_data["description"]) if "description" in company_data else None,
            established_date=(
                EstablishedDate(value=parse_date(company_data["established_date"]))
                if "established_date" in company_data
                else None
            ),
        )

    project_plan: PdfFile | None = None
    if "project_plan" in files:
        project_plan_file: UploadedFile = files["project_plan"]
        project_plan_file.seek(0)
        project_plan = PdfFile(value=project_plan_file.read())

    return ProjectUpdateCommand(
        project_id=Id(value=project_id),
        user_id=Id(value=user_id),
        company=company_update_command,
        name=ProjectName(value=project_data["name"]) if "name" in project_data else None,
        category_id=Id(value=project_data["category_id"]) if "category_id" in project_data else None,
        funding_model_id=Id(value=project_data["funding_model_id"]) if "funding_model_id" in project_data else None,
        stage=ProjectStage(value=project_data["stage"]) if "stage" in project_data else None,
        goal_sum=GoalSum(value=project_data["goal_sum"]) if "goal_sum" in project_data else None,
        deadline=DeadlineDate(value=parse_date(project_data["deadline"])) if "deadline" in project_data else None,
        plan_file=project_plan,
    )
