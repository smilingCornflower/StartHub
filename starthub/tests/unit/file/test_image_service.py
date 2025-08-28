from io import BytesIO

from django.test import SimpleTestCase
from domain.exceptions.file import NotSupportedImageFormatException
from domain.services.file import ImageService
from filetype import filetype
from loguru import logger
from tests.common.check_raises import check_raises
from tests.common.constants import TEST_FILES_PATH


class TestImageServiceCheckImageFormat(SimpleTestCase):
    def setUp(self):
        self.service = ImageService()

    def test_check_image_format_jpeg(self):
        with open(TEST_FILES_PATH / "img.jpg", mode="rb") as f:
            mime = self.service.check_image_format(BytesIO(f.read()))
        self.assertEqual(mime, "image/jpeg")

    def test_check_image_format_png(self):
        with open(TEST_FILES_PATH / "img.png", mode="rb") as f:
            mime = self.service.check_image_format(BytesIO(f.read()))
        self.assertEqual(mime, "image/png")

    def test_check_image_format_gif(self):
        with open(TEST_FILES_PATH / "img.gif", mode="rb") as f:
            mime = self.service.check_image_format(BytesIO(f.read()))
        self.assertEqual(mime, "image/gif")

    def test_check_image_format_webp(self):
        with open(TEST_FILES_PATH / "img.webp", mode="rb") as f:
            mime = self.service.check_image_format(BytesIO(f.read()))
        self.assertEqual(mime, "image/webp")

    def test_check_image_format_avif(self):
        with open(TEST_FILES_PATH / "img.avif", mode="rb") as f:
            mime = self.service.check_image_format(BytesIO(f.read()))
        self.assertEqual(mime, "image/avif")

    def test_check_image_format_unsupported(self):
        exc = NotSupportedImageFormatException
        with self.assertRaises(exc):
            with open(TEST_FILES_PATH / "file.pdf", mode="rb") as f:
                self.service.check_image_format(BytesIO(f.read()))
        check_raises(self.service.check_image_format, exc)


class TestImageConvertToJpg(SimpleTestCase):
    def setUp(self):
        service = ImageService()
        self.service = service

    def test_convert_png_to_jpg(self):
        img_path = TEST_FILES_PATH / "img.png"
        with open(img_path, mode="rb") as img:
            img_data = img.read()
        result = self.service.convert_to_jpg(file_obj=BytesIO(img_data))

        kind = filetype.guess(result)
        self.assertEqual(kind.extension, "jpg")

    def test_convert_webp_to_jpg(self):
        img_path = TEST_FILES_PATH / "img.webp"
        with open(img_path, mode="rb") as img:
            img_data = img.read()
        result = self.service.convert_to_jpg(file_obj=BytesIO(img_data))

        kind = filetype.guess(result)
        self.assertEqual(kind.extension, "jpg")


class TestImageCompress(SimpleTestCase):
    def setUp(self):
        service = ImageService()
        self.service = service

    def test_compress_image(self):
        img_path = TEST_FILES_PATH / "img.png"
        with open(img_path, mode="rb") as img:
            img_data = img.read()
            size_before = len(img_data)
            logger.debug(f"size in bytes before: {size_before}")

        compressed = self.service.compress_image(BytesIO(img_data))
        size_after = len(compressed.read())
        logger.debug(f"size in bytes after: {size_after}")

        self.assertTrue(size_after < size_before)
