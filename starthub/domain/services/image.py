import io
from typing import BinaryIO

from PIL import Image, UnidentifiedImageError
from loguru import logger


class ImageService:
    def convert_to_jpg(self, file_obj: BinaryIO) -> BinaryIO:
        """:raises ValueError:"""
        try:
            return self._convert_to_jpg(file_obj)
        except UnidentifiedImageError as e:
            logger.critical(f"Error during converting an image: {e}")
            raise ValueError("Invalid image format.")

    @staticmethod
    def _convert_to_jpg(file_obj: BinaryIO) -> BinaryIO:
        """:raises UnidentifiedImageError:"""

        output_buffer = io.BytesIO()
        with Image.open(file_obj) as img:
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))

                if img.mode == 'P':
                    img = img.convert('RGBA')

                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background

            elif img.mode != 'RGB':
                img = img.convert('RGB')

            img.save(output_buffer, format='JPEG', quality=100)
        return output_buffer
