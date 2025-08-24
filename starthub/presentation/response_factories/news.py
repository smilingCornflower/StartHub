import pydantic
from domain.exceptions.file import ImageFileTooLargeException, NotSupportedImageFormatException
from domain.exceptions.news import (
    NewsContentIsTooLongException,
    NewsImageContentAndFileMismatchException,
    NewsImageMaxAmountException,
    NewsNotFoundException,
    NewsSubtitleIsTooLongException,
    NewsTitleIsTooLongException,
)
from domain.exceptions.pagination import PaginationMaxLimitException
from domain.exceptions.validation import MissingFileExcpetion
from presentation.response_factories.common import CommonErrorResponseFactory


class NewsErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {
        NotSupportedImageFormatException: ("UNSUPPORTED_IMAGE_FORMAT", 400),
        ImageFileTooLargeException: ("IMAGE_TOO_LARGE", 422),
        NewsTitleIsTooLongException: ("NEWS_TITLE_TOO_LONG", 422),
        NewsSubtitleIsTooLongException: ("NEWS_SUBTITLE_TOO_LONG", 422),
        NewsContentIsTooLongException: ("NEWS_CONTENT_TOO_LONG", 422),
        pydantic.ValidationError: ("INVALID_DATA_TYPE", 400),
        NewsNotFoundException: ("NEWS_NOT_FOUND", 404),
        PaginationMaxLimitException: ("PAGINATION_LIMIT_EXCEEDED", 422),
        MissingFileExcpetion: ("MISSING_FILE", 400),
        NewsImageMaxAmountException: ("TOO_MANY_IMAGES", 422),
        NewsImageContentAndFileMismatchException: ("IMAGE_CONTENT_FILE_MISMATCH", 422),
    }
