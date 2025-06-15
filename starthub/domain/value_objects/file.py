from io import BytesIO

from domain.constants import IMAGE_MAX_SIZE_IN_BYTES, MEGABYTE, PDF_MAX_SIZE_IN_BYTES
from domain.exceptions.file import ImageFileTooLargeException, PdfFileTooLargeException
from domain.services.file import ImageService, PdfService
from domain.value_objects import BaseVo
from pydantic import field_validator


class ImageFile(BaseVo):
    value: bytes

    # noinspection PyNestedDecorators
    @field_validator("value", mode="after")
    @classmethod
    def is_valid_image(cls, value: bytes) -> bytes:
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


class PdfFile(BaseVo):
    value: bytes

    # noinspection PyNestedDecorators
    @field_validator("value", mode="after")
    @classmethod
    def is_valid_pdf(cls, value: bytes) -> bytes:
        """:raises NotPdfFileException:"""
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
