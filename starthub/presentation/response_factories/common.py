from json import JSONDecodeError
from typing import cast

import pydantic
from domain.exceptions.auth import InvalidCredentialsException, PasswordValidationException
from domain.exceptions.company import BusinessNumberAlreadyExistsException, CompanyNameIsTooLongException
from domain.exceptions.file import ImageFileTooLargeException, NotPdfFileException, NotSupportedImageFormatException
from domain.exceptions.geo.city import CityNotFoundException
from domain.exceptions.geo.country import CountryNotFoundException, InvalidCountryCodeException
from domain.exceptions.geo.region import RegionNotFoundException
from domain.exceptions.news import (
    NewsContentIsTooLongException,
    NewsImageContentAndFileMismatchException,
    NewsImagesMaxAmountException,
    NewsNotFoundException,
    NewsTitleIsTooLongException,
)
from domain.exceptions.pagination import PaginationMaxLimitException
from domain.exceptions.permissions import (
    AddDeniedPermissionException,
    DeleteDeniedPermissionException,
    UpdateDeniedPermissionException,
)
from domain.exceptions.project_management import (
    FundingModelNotFoundException,
    InvalidProjectStageException,
    NegativeProjectGoalSumException,
    ProjectCategoryNotFoundException,
    ProjectImageMaxAmountException,
    ProjectNameIsTooLongException,
    ProjectNotFoundException,
    ProjectPlanNotFoundException,
)
from domain.exceptions.user import EmailAlreadyExistsException, UserNotFoundException, UserPhoneAlreadyExistException
from domain.exceptions.user_favorite import UserFavoriteAlreadyExistsException, UserFavoriteNotFoundException
from domain.exceptions.validation import (
    DateInFutureException,
    DeadlineInPastException,
    DisallowedSocialLinkException,
    FirstNameIsTooLongException,
    InvalidEmailException,
    InvalidPhoneNumberException,
    InvalidSocialLinkException,
    LastNameIsTooLongException,
    MissingFileExcpetion,
    StringIsTooLongException,
    ValidationException,
)
from loguru import logger
from presentation.constants import APPLICATION_ERROR_CODES, SUCCESS
from presentation.ports import ErrorResponseFactory
from rest_framework.response import Response


class CommonErrorResponseFactory(ErrorResponseFactory):
    error_codes = APPLICATION_ERROR_CODES

    @classmethod
    def create_response(cls, exception: Exception) -> Response:
        logger.exception(repr(exception))

        for exc_type in type(exception).__mro__:
            if exc_type in cls.error_codes:
                app_code, http_code = cls.error_codes[exc_type]

                if exc_type is pydantic.ValidationError:
                    detail: str = cast(pydantic.ValidationError, exception).errors()[0]["msg"]
                else:
                    detail = str(exception)

                return Response({"detail": detail, "code": app_code}, status=http_code)

        return Response({"detail": "Internal server error", "code": "INTERNAL_ERROR"}, status=500)


class ProjectErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {
        ProjectNameIsTooLongException: ("PROJECT_NAME_TOO_LONG", 422),
        BusinessNumberAlreadyExistsException: ("BUSINESS_NUMBER_ALREADY_EXISTS", 409),
        ProjectCategoryNotFoundException: ("PROJECT_CATEGORY_NOT_FOUND", 404),
        FundingModelNotFoundException: ("FUNDING_MODEL_NOT_FOUND", 404),
        ProjectPlanNotFoundException: ("PROJECT_PLAN_NOT_FOUND", 404),
        CityNotFoundException: ("CITY_NOT_FOUND", 404),
        RegionNotFoundException: ("REGION_NOT_FOUND", 404),
        InvalidProjectStageException: ("INVALID_PROJECT_STAGE", 422),
        NegativeProjectGoalSumException: ("NEGATIVE_GOAL_SUM", 422),
        DisallowedSocialLinkException: ("DISALLOWED_SOCIAL_PLATFORM", 422),
        InvalidSocialLinkException: ("INVALID_SOCIAL_LINK", 422),
        JSONDecodeError: ("JSON_DECODE_ERROR", 400),
        InvalidPhoneNumberException: ("INVALID_PHONE_NUMBER", 422),
        NotPdfFileException: ("NOT_PDF_FILE", 400),
        StringIsTooLongException: ("STRING_TOO_LONG", 422),
        FirstNameIsTooLongException: ("FIRST_NAME_TOO_LONG", 422),
        LastNameIsTooLongException: ("LAST_NAME_TOO_LONG", 422),
        CompanyNameIsTooLongException: ("COMPANY_NAME_TOO_LONG", 422),
        InvalidCountryCodeException: ("INVALID_COUNTRY_CODE", 422),
        CountryNotFoundException: ("COUNTRY_NOT_FOUND", 404),
        DateInFutureException: ("DATE_IN_FUTURE_NOT_ALLOWED", 422),
        ProjectNotFoundException: ("PROJECT_NOT_FOUND", 404),
        DeleteDeniedPermissionException: ("DELETE_PERMISSION_DENIED", 403),
        DeadlineInPastException: ("DEADLINE_IN_PAST", 422),
        UpdateDeniedPermissionException: ("UPDATE_DENIED", 403),
        ProjectImageMaxAmountException: ("TOO_MANY_IMAGES", 422),
        ImageFileTooLargeException: ("IMAGE_TOO_LARGE", 422),
    }


class ReissueAccessErrorResponseFactory(CommonErrorResponseFactory):
    pass


class RegistrationErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {
        InvalidEmailException: ("INVALID_EMAIL", 422),
        EmailAlreadyExistsException: ("EMAIL_ALREADY_EXISTS", 422),
        PasswordValidationException: ("WEAK_PASSWORD", 422),
    }


class LoginErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {
        PasswordValidationException: ("INVALID_PASSWORD_FORMAT", 422),
        ValidationException: ("UNAUTHORIZED", 401),
        InvalidCredentialsException: ("UNAUTHORIZED", 401),
        InvalidEmailException: ("INVALID_EMAIL", 422),
    }


class UserErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {
        UserNotFoundException: ("USER_NOT_FOUND", 404),
        StringIsTooLongException: ("STRING_TOO_LONG", 422),
        NotSupportedImageFormatException: ("UNSUPPORTED_IMAGE_FORMAT", 400),
        pydantic.ValidationError: ("INVALID_DATA_TYPE", 400),
        PasswordValidationException: ("WEAK_PASSWORD", 422),
        UserPhoneAlreadyExistException: ("USER_PHONE_ALREADY_EXISTS", 409),
        InvalidPhoneNumberException: ("INVALID_PHONE_NUMBER", 422),
    }


class UserFavoriteErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {
        # UserFavoriteNotFoundException: ("USER_FAVORITE_NOT_FOUND", 404),
        UserFavoriteNotFoundException: (SUCCESS, 200),  # ignore
        ProjectNotFoundException: ("PROJECT_NOT_FOUND", 404),
        UserFavoriteAlreadyExistsException: ("USER_FAVORITE_ALREADY_EXISTS", 409),
    }


class NewsErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {
        AddDeniedPermissionException: ("ADD_PERMISSION_DENIED", 403),
        UpdateDeniedPermissionException: ("UPDATE_PERMISSION_DENIED", 403),
        NotSupportedImageFormatException: ("UNSUPPORTED_IMAGE_FORMAT", 400),
        ImageFileTooLargeException: ("IMAGE_TOO_LARGE", 422),
        NewsTitleIsTooLongException: ("NEWS_TITLE_TOO_LONG", 422),
        NewsContentIsTooLongException: ("NEWS_CONTENT_TOO_LONG", 422),
        pydantic.ValidationError: ("INVALID_DATA_TYPE", 400),
        NewsNotFoundException: ("NEWS_NOT_FOUND", 404),
        PaginationMaxLimitException: ("PAGINATION_LIMIT_EXCEEDED", 422),
        MissingFileExcpetion: ("MISSING_FILE", 400),
        NewsImagesMaxAmountException: ("TOO_MANY_IMAGES", 422),
        DeleteDeniedPermissionException: ("DELETE_PERMISSION_DENIED", 403),
        NewsImageContentAndFileMismatchException: ("IMAGE_CONTENT_FILE_MISMATCH", 422),
    }
