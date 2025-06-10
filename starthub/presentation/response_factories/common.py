from typing import cast

import pydantic
from domain.exceptions.auth import InvalidCredentialsException, PasswordValidationException
from domain.exceptions.image import NotSupportedImageFormatException
from domain.exceptions.user import EmailAlreadyExistsException
from domain.exceptions.validation import InvalidEmailException, ValidationException
from presentation.constants import APPLICATION_ERROR_CODES
from presentation.ports import ErrorResponseFactory
from rest_framework.response import Response


class CommonErrorResponseFactory(ErrorResponseFactory):
    error_codes = APPLICATION_ERROR_CODES

    @classmethod
    def create_response(cls, exception: Exception) -> Response:
        exception_type = type(exception)

        if exception_type in cls.error_codes:
            app_code, http_code = cls.error_codes[exception_type]

            if exception_type is pydantic.ValidationError:
                detail: str = cast(pydantic.ValidationError, exception).errors()[0]["msg"]
            else:
                detail = str(exception)

            return Response({"detail": detail, "code": app_code}, status=http_code)
        else:
            return Response({"detail": "Internal server error", "code": "INTERNAL_ERROR"}, status=500)


class ProjectErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {
        KeyError: ("MISSING_REQUIRED_FIELD", 400),
    }


class AuthErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {
        InvalidEmailException: ("INVALID_EMAIL", 422),
        ValidationException: ("VALIDATION_EXCEPTION", 422),
        pydantic.ValidationError: ("INVALID_DATA_TYPE", 400),
    }


class RegistrationErrorResponseFactory(AuthErrorResponseFactory):
    error_codes = AuthErrorResponseFactory.error_codes | {
        EmailAlreadyExistsException: ("EMAIL_ALREADY_EXISTS", 422),
        PasswordValidationException: ("WEAK_PASSWORD", 422),
    }


class LoginErrorResponseFactory(AuthErrorResponseFactory):
    error_codes = AuthErrorResponseFactory.error_codes | {
        PasswordValidationException: ("INVALID_PASSWORD_FORMAT", 422),
        ValidationException: ("UNAUTHORIZED", 401),
        InvalidCredentialsException: ("UNAUTHORIZED", 401),
    }


class UserErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {
        NotSupportedImageFormatException: ("UNSUPPORTED_IMAGE_FORMAT", 400),
        pydantic.ValidationError: ("INVALID_DATA_TYPE", 400),
        PasswordValidationException: ("WEAK_PASSWORD", 422),
    }
