from datetime import date
from typing import ClassVar

from domain.constants import CHAR_FIELD_MAX_LENGTH, NEWS_CONTENT_MAX_LENGTH, NEWS_IMAGES_MAX_AMOUNT
from domain.enums.news_tag import NewsTagEnum
from domain.exceptions import CustomException
from domain.exceptions.news import (
    NewsContentIsTooLongException,
    NewsImageMaxAmountException,
    NewsSubtitleIsTooLongException,
    NewsTitleIsTooLongException,
)
from domain.ports.command import BaseCommand
from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects.common import Id, StringVo
from domain.value_objects.file import Image
from pydantic import field_validator


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
    is_active: bool | None = None


class NewsGetCommand(BaseCommand):
    published_at_start: date | None = None
    published_at_end: date | None = None


class NewsCreateCommand(BaseCommand):
    title: NewsTitle
    subtitle: NewsSubtitle | None
    content: NewsContent
    author_id: Id
    cover: Image
    images: list[Image]
    tags: list[NewsTagEnum] | None

    @field_validator("images", mode="after")
    @classmethod
    def validate_images_amount(cls, images: list[Image]) -> list[Image]:
        """:rasies NewsImagesMaxAmountException"""
        if len(images) > NEWS_IMAGES_MAX_AMOUNT:
            raise NewsImageMaxAmountException(f"News images max limit is {NEWS_IMAGES_MAX_AMOUNT}.")
        return images


class NewsUpdateCommand(BaseCommand):
    title: NewsTitle | None = None
    subtitle: NewsSubtitle | None = None
    content: NewsContent | None = None
    cover: Image | None = None
    images: list[Image] | None = None
