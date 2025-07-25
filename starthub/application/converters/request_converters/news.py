from typing import Any, cast

from django.core.files.uploadedfile import UploadedFile
from django.utils.datastructures import MultiValueDict
from loguru import logger

from application.converters.request_converters.common import get_required_field
from domain.value_objects.common import Id
from domain.value_objects.file import Image, ImageFile
from domain.value_objects.filter import NewsFilter
from domain.value_objects.news import NewsContent, NewsCreateCommand, NewsTitle, NewsUpdateCommand


def request_to_news_create_command(
    request_data: dict[str, Any], request_files: MultiValueDict[str, UploadedFile], user_id: int
) -> NewsCreateCommand:
    """
    :raises MissingRequiredFieldException:
    :raises NotSupportedImageFormatException:
    """

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
        content=NewsContent(value=get_required_field(request_data, "content")),
        author_id=Id(value=user_id),
        cover=cover,
        images=news_images,
    )


def request_to_news_update_command(
    request_data: dict[str, Any], request_files: MultiValueDict[str, UploadedFile], news_id: int, user_id: int
) -> NewsUpdateCommand:
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

    return NewsUpdateCommand(
        user_id=Id(value=user_id),
        news_id=Id(value=news_id),
        title=NewsTitle(value=request_data["title"]) if "title" in request_data else None,
        content=NewsContent(value=request_data["content"]) if "content" in request_data else None,
        cover=cover,
        images=images,
    )


def request_to_news_filter(request_data: dict[str, Any]) -> NewsFilter:
    return NewsFilter()
