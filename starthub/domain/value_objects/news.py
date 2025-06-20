from domain.constants import CHAR_FIELD_MAX_LENGTH, NEWS_CONTENT_MAX_LENGTH
from domain.exceptions.news import NewsContentIsTooLongException, NewsTitleIsTooLongException
from domain.exceptions.validation import EmptyStringException
from domain.ports.command import BaseCommand
from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects import BaseVo
from domain.value_objects.common import Id
from domain.value_objects.file import ImageFile
from pydantic import field_validator


class NewsTitle(BaseVo):
    value: str

    # noinspection PyNestedDecorators
    @field_validator("value", mode="after")
    @classmethod
    def is_valid_name(cls, value: str) -> str:
        """
        :raises EmptyStringException:
        :raises NewsTitleIsTooLongException:
        """
        if not value:
            raise EmptyStringException("News title cannot be empty.")
        if len(value) > CHAR_FIELD_MAX_LENGTH:
            raise NewsTitleIsTooLongException(f"News title must be at most {CHAR_FIELD_MAX_LENGTH} characters long.")
        return value


class NewsContent(BaseVo):
    value: str

    # noinspection PyNestedDecorators
    @field_validator("value", mode="after")
    @classmethod
    def is_valid_name(cls, value: str) -> str:
        """
        :raises EmptyStringException:
        :raises NewsContentIsTooLongException:
        """
        if not value:
            raise EmptyStringException("News title cannot be empty.")
        if len(value) > NEWS_CONTENT_MAX_LENGTH:
            raise NewsContentIsTooLongException(
                f"New content must be at most {NEWS_CONTENT_MAX_LENGTH} characters long."
            )

        return value


class NewsCreatePayload(AbstractCreatePayload):
    title: NewsTitle
    content: NewsContent
    author_id: Id
    image_url: str


class NewsUpdatePayload(AbstractUpdatePayload):
    news_id: Id
    title: NewsTitle | None = None
    content: NewsContent | None = None
    image_url: str | None = None


class NewsCreateCommand(BaseCommand):
    title: NewsTitle
    content: NewsContent
    author_id: Id
    image: ImageFile


class NewsUpdateCommand(BaseCommand):
    news_id: Id
    title: NewsTitle | None = None
    content: NewsContent | None = None
    image: ImageFile | None = None


class NewsImageUploadCommand(BaseCommand):
    image: ImageFile
