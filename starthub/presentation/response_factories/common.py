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
            return Response({"detail": str(exception), "code": app_code}, status=http_code)
        else:
            return Response({"detail": "Internal server error", "code": "INTERNAL_ERROR"}, status=500)


class ProjectErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {KeyError: ("MISSING_REQUIRED_FIELD", 400)}
