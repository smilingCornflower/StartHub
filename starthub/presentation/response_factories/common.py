from typing import cast

import pydantic
from loguru import logger
from presentation.constants import APPLICATION_ERROR_CODES
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
