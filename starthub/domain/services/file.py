import io
from io import BytesIO
from typing import BinaryIO

import filetype
from domain.exceptions.file import NotPdfFileException, NotSupportedImageFormatException
from domain.ports.service import AbstractDomainService
from loguru import logger
from wand.image import Image


class ImageService(AbstractDomainService):
    IMAGE_FORMATS = ("image/jpeg", "image/png", "image/gif", "image/webp", "image/avif")

    def check_image_format(self, file_obj: BinaryIO) -> None:
        """
        :raises  NotSupportedImageFormatException:
        """
        kind = filetype.guess(file_obj)

        if kind is None:
            logger.debug("Failed to identify file type.")
            raise NotSupportedImageFormatException(f"Unrecognized file type. Expected: {', '.join(self.IMAGE_FORMATS)}")

        logger.debug(f"king.mime = {kind.mime}")
        if kind.mime not in self.IMAGE_FORMATS:
            raise NotSupportedImageFormatException(
                f"The image format {kind.mime} is not supported. "
                f"Supported image formats: {', '.join(self.IMAGE_FORMATS)}"
            )

    def convert_to_jpg(self, file_obj: BinaryIO) -> BytesIO:
        """
        :raises NotSupportedImageFormatException:
        """
        self.check_image_format(file_obj)
        result = io.BytesIO()

        with Image(file=file_obj) as img:
            with img.convert("jpg") as converted:
                converted.save(file=result)
        return result


class PdfService(AbstractDomainService):
    def check_is_pdf(self, file_obj: BinaryIO) -> None:
        """:raises NotPdfFileException:"""

        kind = filetype.guess(file_obj)
        if kind is None:
            logger.debug("Failed to identify file type.")
            raise NotPdfFileException("Unrecognized file type, expected pdf file.")
        logger.debug(f"king.mime = {kind.mime}")
        if kind.mime != "application/pdf":
            raise NotPdfFileException(f"The file format: {kind.mime} is not supported, allowed pdf file only.")
