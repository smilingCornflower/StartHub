from io import BytesIO
from pathlib import Path

import filetype
from config.settings import BASE_DIR
from django.test import SimpleTestCase
from domain.exceptions.image import NotSupportedImageFormatException
from domain.services.image import ImageService
from loguru import logger


class TestImageService(SimpleTestCase):
    supported_image_files: list[Path]
    not_image_files: list[Path]
    unsupported_images: list[Path]

    @classmethod
    def setUpClass(cls) -> None:
        cls.supported_image_files = [
            BASE_DIR / "tests/images/miku.jpg",
            BASE_DIR / "tests/images/Kawaii.png",
            BASE_DIR / "tests/images/artwork.png",
            BASE_DIR / "tests/images/tokyo-city.webp",
            BASE_DIR / "tests/images/fox-boy.avif",
            BASE_DIR / "tests/images/chika.gif",
        ]
        cls.not_image_files = [
            BASE_DIR / "tests/files/The_C_Programming_Language.pdf",
            BASE_DIR / "tests/files/articles.docx",
            BASE_DIR / "tests/files/articles.jpg",
        ]
        cls.unsupported_images = [
            BASE_DIR / "tests/images/galaxy.tiff",
            BASE_DIR / "tests/images/angel.bmp",
            BASE_DIR / "tests/images/Alice.svg",
        ]

    def test_correct_image_formats(self) -> None:
        for i in self.supported_image_files:
            with self.subTest(file=i.suffix):
                with open(i, mode="rb") as img_file:
                    ImageService()._check_image_format(img_file)

    def test_invalid_image_files(self) -> None:
        for i in self.not_image_files:
            with self.assertRaises(NotSupportedImageFormatException):
                logger.info(i)
                with open(i, mode="rb") as f:
                    ImageService()._check_image_format(f)

    def test_convert_to_jpg(self) -> None:
        for i in self.supported_image_files:
            with self.subTest(file=i.name):
                with open(i, mode="rb") as img_file:
                    converted: BytesIO = ImageService().convert_to_jpg(img_file)
                kind = filetype.guess(converted)
                self.assertEqual(kind.mime, "image/jpeg")
