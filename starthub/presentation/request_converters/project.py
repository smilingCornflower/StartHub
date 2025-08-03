import json
from pprint import pformat
from typing import cast

from application.converters.request_converters.project import (
    _request_data_to_company_founder_create_command,
    _request_data_to_team_members,
    _request_files_to_project_plan,
)
from django.core.files.uploadedfile import UploadedFile
from django.http import QueryDict
from domain.value_objects.common import DeadlineDate, Description, Id, PhoneNumber, Slug, SocialLink
from domain.value_objects.company import BusinessNumber, CompanyName, EstablishedDate
from domain.value_objects.country import CountryCode
from domain.value_objects.file import ImageFile, PdfFile
from domain.value_objects.filter import ProjectFilter
from domain.value_objects.project_management import (
    GoalSum,
    ProjectCreateCommand,
    ProjectName,
    ProjectStage,
    ProjectStatus,
)
from loguru import logger
from presentation.request_converters.common import get_required_field, parse_date
from rest_framework.request import Request


def request_data_to_project_create_command(request: Request, user_id: int) -> ProjectCreateCommand:
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
    data = request.data
    files = request.FILES

    project_data = json.loads(get_required_field(data, field="project"))
    company_data = json.loads(get_required_field(data, field="company"))
    project_plan: PdfFile = _request_files_to_project_plan(files=files)
    country_code = CountryCode(value=get_required_field(company_data, "country_code", "company.country_code"))
    project_images: list[ImageFile] = list()

    images: list[UploadedFile] = files.getlist("images")
    for image in images:
        image.seek(0)
        project_images.append(ImageFile(value=image.read()))
    logger.debug("request.FILES -> ImageFile conversion OK")

    command = ProjectCreateCommand(
        name=ProjectName(value=get_required_field(project_data, field="name")),
        creator_id=Id(value=user_id),
        description=Description(value=get_required_field(project_data, field="description")),
        category_ids=[Id(value=i) for i in get_required_field(project_data, "category_ids")],
        funding_model_id=Id(value=get_required_field(project_data, field="funding_model_id")),
        stage=ProjectStage(value=get_required_field(project_data, field="stage")),
        goal_sum=GoalSum(value=get_required_field(project_data, field="goal_sum")),
        deadline=DeadlineDate(value=parse_date(get_required_field(project_data, field="deadline"))),
        social_links=[
            SocialLink(platform=k, link=v) for k, v in get_required_field(project_data, "social_links").items()
        ],
        phone_number=PhoneNumber(value=get_required_field(project_data, "phone_number")),
        plan_file=project_plan,
        images=project_images,
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
    logger.debug(f"command: \n{pformat(command.__dict__)}")
    return command


def convert_request_to_project_filter(request: Request) -> ProjectFilter:
    params: QueryDict = request.query_params
    logger.debug(f"params = {pformat(params)}")

    filter_ = ProjectFilter()
    if params.get("category_slug"):
        filter_.category_slug = Slug(value=cast(str, params.get("category_slug")))
    if params.get("funding_model_slug"):
        filter_.funding_model_slug = Slug(value=cast(str, params.get("funding_model_slug")))
    if params.get("status"):
        filter_.status = ProjectStatus(value=cast(str, params.get("status")))
    if params.get("stage"):
        filter_.stage = ProjectStage(value=cast(str, params.get("stage")))
    if params.get("user_id"):
        filter_.user_id = Id(value=int(cast(str, params["user_id"])))

    return filter_
