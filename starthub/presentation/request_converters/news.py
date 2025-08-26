from pprint import pformat
from typing import Any, cast

from django.core.files.uploadedfile import UploadedFile
from django.utils.datastructures import MultiValueDict
from domain.value_objects.common import Id
from domain.value_objects.file import Image, ImageFile
from domain.value_objects.news import (
    NewsContent,
    NewsCreateCommand,
    NewsGetCommand,
    NewsSubtitle,
    NewsTitle,
    NewsUpdateCommand,
)
from loguru import logger
from presentation.request_converters.common import get_required_field, parse_date
from rest_framework.request import Request


def request_to_news_create_command(request: Request, user_id: Id) -> NewsCreateCommand:
    """
    :raises MissingRequiredFieldException:
    :raises NotSupportedImageFormatException:
    """
    request_data: dict[str, Any] = request.data
    request_files: MultiValueDict[str, UploadedFile] = request.FILES

    cover_file: UploadedFile = get_required_field(request_files, "cover")
    cover_file.seek(0)
    cover = Image(
        name=cover_file.name if cover_file.name else "default_cover_name", file=ImageFile(value=cover_file.read())
    )

    images: list[UploadedFile] = request_files.getlist("images")
    news_images: list[Image] = list()
    for img in images:
        img.seek(0)
        news_images.append(Image(name=img.name if img.name else "default_image_name", file=ImageFile(value=img.read())))
        logger.debug(f"image = {img.name} added.")

    return NewsCreateCommand(
        title=NewsTitle(value=get_required_field(request_data, "title")),
        subtitle=NewsSubtitle(value=request_data["subtitle"]) if "subtitle" in request_data else None,
        content=NewsContent(value=get_required_field(request_data, "content")),
        author_id=user_id,
        cover=cover,
        images=news_images,
    )


def request_to_news_update_command(request: Request) -> NewsUpdateCommand:
    request_data: dict[str, Any] = request.data
    request_files: MultiValueDict[str, UploadedFile] = request.FILES

    images: list[Image] | None = None
    if "images" in request_files:
        images = list()
        for img in request_files.getlist("images"):
            img.seek(0)
            images.append(Image(name=img.name if img.name else "default_image_name", file=ImageFile(value=img.read())))

    cover: Image | None = None
    if "cover" in request_files:
        cover_file = cast(UploadedFile, request_files.get("cover"))
        cover = Image(
            name=cover_file.name if cover_file.name else "default_cover_name", file=ImageFile(value=cover_file.read())
        )

    command = NewsUpdateCommand(
        title=NewsTitle(value=request_data["title"]) if "title" in request_data else None,
        subtitle=NewsSubtitle(value=request_data["subtitle"]) if "subtitle" in request_data else None,
        content=NewsContent(value=request_data["content"]) if "content" in request_data else None,
        cover=cover,
        images=images,
    )
    logger.debug(f"update_command: \n{pformat(command.__dict__)}")
    return command


def request_to_news_get_command(request: Request) -> NewsGetCommand:
    params = request.query_params
    command = NewsGetCommand(
        published_at_start=parse_date(params["published_at_start"]) if "published_at_start" in params else None,
        published_at_end=parse_date(params["published_at_end"]) if "published_at_end" in params else None,
    )
    logger.debug(f"command = {command}")
    return command
