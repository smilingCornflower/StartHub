from dataclasses import dataclass

from django.test import SimpleTestCase
from domain.exceptions.file import NotSupportedImageFormatException
from domain.value_objects.file import ImageFile, JpgImage
from tests.common.constants import TEST_FILES_PATH
from tests.utils import check_raises


@dataclass
class JpgImageTestData:
    _valid_jpg_content = None
    _png_content = None
    _pdf_content = None
    name = "img.jpg"

    @property
    def valid_jpg_content(self):
        if self._valid_jpg_content is None:
            with open(TEST_FILES_PATH / "img.jpg", mode="rb") as f:
                self._valid_jpg_content = f.read()
        return self._valid_jpg_content

    @property
    def png_content(self):
        if self._png_content is None:
            with open(TEST_FILES_PATH / "img.png", mode="rb") as f:
                self._png_content = f.read()
        return self._png_content

    @property
    def pdf_content(self):
        if self._pdf_content is None:
            with open(TEST_FILES_PATH / "file.pdf", mode="rb") as f:
                self._pdf_content = f.read()
        return self._pdf_content


class TestJpgImage(SimpleTestCase):
    def setUp(self):
        self.data = JpgImageTestData()

    def test_valid_jpg(self):
        jpg_image = JpgImage(file=ImageFile(value=self.data.valid_jpg_content), name=self.data.name)

        self.assertEqual(jpg_image.file.value, self.data.valid_jpg_content)

    def test_png_raises_not_supported_format(self):
        exc = NotSupportedImageFormatException

        check_raises(JpgImage.validate_jpg, exc)
        with self.assertRaises(exc):
            JpgImage(file=ImageFile(value=self.data.png_content), name=self.data.name)

    def test_pdf_raises_not_supported_format(self):
        exc = NotSupportedImageFormatException

        check_raises(JpgImage.validate_jpg, exc)
        with self.assertRaises(exc):
            JpgImage(file=ImageFile(value=self.data.pdf_content), name=self.data.name)
