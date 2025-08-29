from io import BytesIO

from domain.constants import IMAGE_MAX_SIZE_IN_BYTES, MEGABYTE, PDF_MAX_SIZE_IN_BYTES
from domain.enums.image_kind import ImageKindEnum
from domain.exceptions.file import (
    ImageFileTooLargeException,
    NotSupportedImageFormatException,
    PdfFileTooLargeException,
)
from domain.services.file import ImageService, PdfService
from domain.value_objects import BaseVo
from filetype import guess
from loguru import logger
from pydantic import field_validator


class FileVo(BaseVo):
    value: bytes

    def __str__(self) -> str:
        return f"{self.__class__.__name__} {len(self.value)} bytes"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(bytes_len={len(self.value)})"


class ImageFile(FileVo):
    # noinspection PyNestedDecorators
    @field_validator("value", mode="after")
    @classmethod
    def validate_image(cls, value: bytes) -> bytes:
        """
        :raises ImageFileTooLargeException:
        :raises NotSupportedImageFormatException:
        """
        if len(value) > IMAGE_MAX_SIZE_IN_BYTES:
            raise ImageFileTooLargeException(
                f"image size {round(len(value) / MEGABYTE, 1)} MB exceeds max allowed {IMAGE_MAX_SIZE_IN_BYTES // MEGABYTE} MB."
            )
        ImageService().check_image_format(BytesIO(value))
        return value

    def __str__(self) -> str:
        return f"ImageFile {len(self.value)} bytes"

    def __repr__(self) -> str:
        return f"ImageFile(bytes_len={len(self.value)})"


class Image(BaseVo):
    name: str
    file: ImageFile


class JpgImage(Image):
    # noinspection PyNestedDecorators
    @field_validator("file", mode="after")
    @classmethod
    def validate_jpg(cls, file: ImageFile) -> ImageFile:
        """:raises NotSupportedImageFormatException:"""
        kind = guess(file.value)
        if kind.mime != ImageKindEnum.JPEG:
            logger.exception("Not a jpeg file")
            raise NotSupportedImageFormatException("Only jpeg image allowed.")
        return file


class PdfFile(FileVo):
    # noinspection PyNestedDecorators
    @field_validator("value", mode="after")
    @classmethod
    def validate_pdf(cls, value: bytes) -> bytes:
        """
        :raises NotPdfFileException:
        :raises PdfFileTooLargeException:
        """
        if len(value) > PDF_MAX_SIZE_IN_BYTES:
            raise PdfFileTooLargeException(
                f"pdf size {round(len(value) / MEGABYTE, 1)} MB exceeds max allowed {PDF_MAX_SIZE_IN_BYTES // MEGABYTE} MB."
            )

        PdfService().check_is_pdf(BytesIO(value))
        return value

    def __str__(self) -> str:
        return f"PdfFile {len(self.value)} bytes"

    def __repr__(self) -> str:
        return f"PdfFile(bytes_len={len(self.value)})"
