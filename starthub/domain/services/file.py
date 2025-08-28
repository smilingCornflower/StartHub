import io
import os
import shutil
import tempfile
from io import BytesIO
from typing import BinaryIO, cast

import filetype
from domain.constants import IMAGE_COMPRESSION_QUALITY, TEMP_FILE_PATH, VIDEO_COMPRESSION_BITRATE
from domain.exceptions.file import NotPdfFileException, NotSupportedImageFormatException
from domain.ports.service import AbstractDomainService
from loguru import logger
from moviepy import VideoFileClip
from wand.image import Image


class ImageService(AbstractDomainService):
    IMAGE_FORMATS = ("image/jpeg", "image/png", "image/gif", "image/webp", "image/avif")

    def check_image_format(self, file_obj: BinaryIO) -> str:
        """
        :raises NotSupportedImageFormatException:
        """
        kind = filetype.guess(file_obj)

        if kind is None:
            logger.debug("Failed to identify file type.")
            raise NotSupportedImageFormatException(f"Unrecognized file type. Expected: {', '.join(self.IMAGE_FORMATS)}")

        logger.debug(f"kind.mime = {kind.mime}")
        if kind.mime not in self.IMAGE_FORMATS:
            raise NotSupportedImageFormatException(
                f"The image format {kind.mime} is not supported. "
                f"Supported image formats: {', '.join(self.IMAGE_FORMATS)}"
            )
        return cast(str, kind.mime)

    def convert_to_jpg(self, file_obj: BinaryIO) -> BytesIO:
        """
        :raises NotSupportedImageFormatException:
        """
        self.check_image_format(file_obj)
        result = io.BytesIO()

        with Image(file=file_obj) as img:
            with img.convert("jpg") as converted:
                converted.save(file=result)
        result.seek(0)
        return result

    @staticmethod
    def compress_image(file_obj: BinaryIO) -> BinaryIO:
        with Image(file=file_obj) as img:
            out = BytesIO()
            img.compression_quality = IMAGE_COMPRESSION_QUALITY
            img.save(file=out)
            out.seek(0)
            return out


class PdfService(AbstractDomainService):
    @staticmethod
    def check_is_pdf(file_obj: BinaryIO) -> None:
        """:raises NotPdfFileException:"""

        kind = filetype.guess(file_obj)
        if kind is None:
            logger.debug("Failed to identify file type.")
            raise NotPdfFileException("Unrecognized file type, expected pdf file.")
        logger.debug(f"king.mime = {kind.mime}")
        if kind.mime != "application/pdf":
            raise NotPdfFileException(f"The file format: {kind.mime} is not supported, allowed pdf file only.")


class VideoService(AbstractDomainService):
    @staticmethod
    def compress_video(file_obj: BinaryIO) -> BinaryIO:
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_in:
            shutil.copyfileobj(file_obj, temp_in)
            input_path = temp_in.name

        output_path = None

        with VideoFileClip(input_path) as clip:
            original_bitrate: int = clip.reader.bitrate
            logger.debug(f"original_bitrate = {original_bitrate}")

            if original_bitrate <= VIDEO_COMPRESSION_BITRATE:
                logger.debug("Compression skipped - original bitrate is low enough")
                out = file_obj
            else:
                with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_out:
                    output_path = temp_out.name

                clip.write_videofile(
                    output_path,
                    bitrate=f"{VIDEO_COMPRESSION_BITRATE}k",
                    codec="libx264",
                    temp_audiofile_path=TEMP_FILE_PATH,
                )
                with open(output_path, "rb") as f:
                    out = BytesIO(f.read())

        out.seek(0)
        os.remove(input_path)
        if output_path:
            os.remove(output_path)

        return out
