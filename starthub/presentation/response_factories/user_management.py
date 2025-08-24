import pydantic
from domain.exceptions.auth import InvalidCredentialsException, PasswordValidationException
from domain.exceptions.file import NotSupportedImageFormatException
from domain.exceptions.project_management import ProjectNotFoundException
from domain.exceptions.role import RoleNotFoundException
from domain.exceptions.user import EmailAlreadyExistsException, UserNotFoundException, UserPhoneAlreadyExistException
from domain.exceptions.user_favorite import UserFavoriteAlreadyExistsException, UserFavoriteNotFoundException
from domain.exceptions.user_message import (
    UserMessageContentIsTooLongException,
    UserMessageNotFoundException,
    UserMessageTopicIsTooLongException,
)
from domain.exceptions.validation import (
    EmptyStringException,
    FirstNameIsTooLongException,
    InvalidEmailException,
    InvalidPhoneNumberException,
    LastNameIsTooLongException,
    StringIsTooLongException,
    ValidationException,
)
from presentation.constants import SUCCESS
from presentation.response_factories.common import CommonErrorResponseFactory
from domain.exceptions.user_message import UserUnreadMessageMaxAmountException


class UsersAdminErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {
        RoleNotFoundException: ("ROLE_NOT_FOUND", 404),
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


class UserMessageErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {
        UserMessageNotFoundException: ("USER_MESSAGE_NOT_FOUND", 404),
        UserUnreadMessageMaxAmountException: ("MAX_UNREAD_MESSAGES_AMOUNT_EXCEEDED", 422),
        FirstNameIsTooLongException: ("FIRST_NAME_TOO_LONG", 422),
        LastNameIsTooLongException: ("LAST_NAME_TOO_lONG", 422),
        EmptyStringException: ("EMPTY_VALUE_NOT_ALLOWED", 422),
        InvalidEmailException: ("INVALID_EMAIL", 422),
        InvalidPhoneNumberException: ("INVALID_PHONE_NUMBER", 422),
        UserMessageTopicIsTooLongException: ("MESSAGE_TOPIC_TOO_LONG", 422),
        UserMessageContentIsTooLongException: ("MESSAGE_CONTENT_TOO_LONG", 422),
    }
