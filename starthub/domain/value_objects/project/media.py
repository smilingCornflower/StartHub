from domain import constants
from domain.constants import IMAGE_MAX_SIZE_IN_BYTES, MEDIA_SUPPORTED_FILES_FORMATS, MEGABYTE, VIDEO_MAX_SIZE_IN_BYTES
from domain.exceptions.file import (
    ImageFileTooLargeException,
    UnsupportedFileExtensionException,
    VideoFileTooLargeException,
)
from domain.ports.command import BaseCommand
from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects.common import Id, Order
from domain.value_objects.file import FileVo
from filetype import guess
from loguru import logger
from pydantic import field_validator


class MediaFile(FileVo):

    @property
    def file_extension(self) -> str:
        kind = guess(self.value)
        return str(kind.extension)

    # noinspection PyNestedDecorators
    @field_validator("value", mode="after")
    @classmethod
    def _validate_file_extesnsion(cls, value: bytes) -> bytes:
        """Validates file type and returns file extension"""
        kind = guess(value)
        file_ext: str | None = kind.extension if kind else None
        logger.debug(f"MediaFile extensioin = {file_ext}")

        if file_ext not in MEDIA_SUPPORTED_FILES_FORMATS:
            logger.exception(f"Unsupported file type: {file_ext}. Expected: {', '.join(MEDIA_SUPPORTED_FILES_FORMATS)}")
            raise UnsupportedFileExtensionException(
                f"Unsupported file type: {file_ext}. Expected: {', '.join(MEDIA_SUPPORTED_FILES_FORMATS)}"
            )
        return value

    @field_validator("value", mode="after")
    @classmethod
    def validate_file_size(cls, value: bytes) -> bytes:
        kind = guess(value)
        file_ext: str | None = kind.extension if kind else None

        logger.debug(f"file size = {len(value)}")

        if file_ext in constants.IMAGE_FILE_FORMATS:
            if len(value) > IMAGE_MAX_SIZE_IN_BYTES:
                raise ImageFileTooLargeException(
                    f"image size {round(len(value) / MEGABYTE, 1)} MB exceeds max allowed {IMAGE_MAX_SIZE_IN_BYTES // MEGABYTE} MB."
                )
        elif file_ext in constants.VIDEO_FILE_FORMATS:
            if len(value) > VIDEO_MAX_SIZE_IN_BYTES:
                raise VideoFileTooLargeException(
                    f"video size {round(len(value) / MEGABYTE, 1)} MB exceeds max allowed {IMAGE_MAX_SIZE_IN_BYTES // MEGABYTE} MB."
                )
        return value


class ProjectMediaId(Id):
    pass


class ProjectMediaCreatePayload(AbstractCreatePayload):
    project_id: Id
    file_path: str
    order: int


class ProjectMediaUpdatePayload(AbstractUpdatePayload):
    media_id: ProjectMediaId
    order: Order


class ProjectMediaCreateCommand(BaseCommand):
    media: MediaFile


class ProjectMediaUpdateCommand(BaseCommand):
    new_order: list[Order] | None
