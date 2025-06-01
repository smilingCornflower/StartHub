from domain.exceptions.auth import InvalidCredentialsException, InvalidTokenException, TokenExpiredException
from domain.exceptions.company import CompanyNotFoundException, CompanyOwnershipRequiredException
from domain.exceptions.permissions import DeletePermissionDenied
from domain.exceptions.project_management import (
    FundingModelNotFoundException,
    NegativeProjectGoalSumValidationException,
    ProjectCategoryNotFoundException,
    ProjectDeadlineInPastValidationException,
    ProjectNameIsTooLongValidationException,
)
from domain.exceptions.user import UserNotFoundException
from domain.exceptions.validation import (
    DateIsNotIsoFormatException,
    DisallowedSocialLinkException,
    EmptyStringException,
    FirstNameIsTooLongException,
    InvalidPhoneNumberException,
    InvalidSocialLinkException,
    LastNameIsTooLongException,
)

APPLICATION_ERROR_CODES: dict[type, tuple[str, int]] = {
    # 404 Not Found Errors
    UserNotFoundException: ("USER_NOT_FOUND", 404),
    CompanyNotFoundException: ("COMPANY_NOT_FOUND", 404),
    ProjectCategoryNotFoundException: ("PROJECT_CATEGORY_NOT_FOUND", 404),
    FundingModelNotFoundException: ("FUNDING_MODEL_NOT_FOUND", 404),
    # 403 Forbidden
    CompanyOwnershipRequiredException: ("COMPANY_OWNERSHIP_REQUIRED", 403),
    DeletePermissionDenied: ("DELETE_PERMISSION_DENIED", 403),
    # 422 Unprocessable Entity
    ProjectNameIsTooLongValidationException: ("PROJECT_NAME_TOO_LONG", 422),
    NegativeProjectGoalSumValidationException: ("NEGATIVE_GOAL_SUM", 422),
    ProjectDeadlineInPastValidationException: ("DEADLINE_IN_PAST", 422),
    FirstNameIsTooLongException: ("FIRST_NAME_TOO_LONG", 422),
    LastNameIsTooLongException: ("LAST_NAME_TOO_LONG", 422),
    EmptyStringException: ("EMPTY_VALUE_NOT_ALLOWED ", 422),
    InvalidPhoneNumberException: ("INVALID_PHONE_NUMBER", 422),
    InvalidSocialLinkException: ("INVALID_SOCIAL_LINK", 422),
    DisallowedSocialLinkException: ("DISALLOWED_SOCIAL_PLATFORM", 422),
    DateIsNotIsoFormatException: ("DATE_IS_NOT_ISO_FORMAT", 422),
    # 401 Unauthorized
    InvalidCredentialsException: ("INVALID_CREDENTIALS", 401),
    InvalidTokenException: ("INVALID_TOKEN", 401),
    TokenExpiredException: ("TOKEN_EXPIRED", 401),
}
