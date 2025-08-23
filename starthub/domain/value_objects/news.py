from typing import ClassVar

from pydantic import field_validator

from domain.constants import CHAR_FIELD_MAX_LENGTH, NEWS_CONTENT_MAX_LENGTH, NEWS_IMAGES_MAX_AMOUNT
from domain.exceptions import CustomException
from domain.exceptions.news import (
    NewsContentIsTooLongException,
    NewsImagesMaxAmountException,
    NewsSubtitleIsTooLongException,
    NewsTitleIsTooLongException,
)
from domain.ports.command import BaseCommand
from domain.ports.payload import AbstractCreatePayload, AbstractDeletePayload, AbstractUpdatePayload
from domain.value_objects.common import Id, StringVo
from domain.value_objects.file import Image, ImageFile


class NewsTitle(StringVo):
    max_length: ClassVar[int] = CHAR_FIELD_MAX_LENGTH
    too_long_string_exception: ClassVar[type[CustomException]] = NewsTitleIsTooLongException


class NewsSubtitle(StringVo):
    max_length: ClassVar[int] = CHAR_FIELD_MAX_LENGTH
    too_long_string_exception: ClassVar[type[CustomException]] = NewsSubtitleIsTooLongException


class NewsContent(StringVo):
    max_length: ClassVar[int] = NEWS_CONTENT_MAX_LENGTH
    too_long_string_exception: ClassVar[type[CustomException]] = NewsContentIsTooLongException


class NewsCreatePayload(AbstractCreatePayload):
    title: NewsTitle
    subtitle: NewsSubtitle | None
    content: NewsContent
    author_id: Id


class NewsUpdatePayload(AbstractUpdatePayload):
    news_id: Id
    title: NewsTitle | None = None
    subtitle: NewsSubtitle | None = None
    content: NewsContent | None = None
    cover_path: str | None = None


class NewsCreateCommand(BaseCommand):
    title: NewsTitle
    subtitle: NewsSubtitle | None
    content: NewsContent
    author_id: Id
    cover: Image
    images: list[Image]

    @field_validator("images", mode="after")
    @classmethod
    def validate_images_amount(cls, images: list[Image]) -> list[Image]:
        """:rasies NewsImagesMaxAmountException"""
        if len(images) > NEWS_IMAGES_MAX_AMOUNT:
            raise NewsImagesMaxAmountException(f"News images max limit is {NEWS_IMAGES_MAX_AMOUNT}.")
        return images


class NewsUpdateCommand(BaseCommand):
    title: NewsTitle | None = None
    subtitle: NewsSubtitle | None = None
    content: NewsContent | None = None
    cover: Image | None = None
    images: list[Image] | None = None


class NewsImageUploadCommand(BaseCommand):
    image: ImageFile


class NewsImageCreatePayload(AbstractCreatePayload):
    news_id: Id
    image: str


class NewsImageUpdatePayload(AbstractUpdatePayload):
    pass


class NewsImageDeletePayload(AbstractDeletePayload):
    file_name: str
