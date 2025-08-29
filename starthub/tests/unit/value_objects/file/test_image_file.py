from dataclasses import dataclass

from django.test import SimpleTestCase
from domain.exceptions.file import ImageFileTooLargeException, NotSupportedImageFormatException
from domain.value_objects.file import IMAGE_MAX_SIZE_IN_BYTES, ImageFile
from tests.common.constants import TEST_FILES_PATH
from tests.utils import check_raises
from win32inetcon import NORMAL_CACHE_ENTRY


@dataclass
class ImageFileTestData:
    _valid_image_content = None
    _too_large_image_content = None
    _file_pdf_content = None

    @property
    def valid_image_content(self):
        if self._valid_image_content is None:
            with open(TEST_FILES_PATH / "img.jpg", mode="rb") as f:
                self._valid_image_content = f.read()
        return self._valid_image_content

    @property
    def too_large_image_content(self):
        if self._too_large_image_content is None:
            with open(TEST_FILES_PATH / "large_img.png", mode="rb") as f:
                self._too_large_image_content = f.read()
        return self._too_large_image_content

    @property
    def file_pdf_content(self):
        if self._file_pdf_content is None:
            with open(TEST_FILES_PATH / "file.pdf", mode="rb") as f:
                self._file_pdf_content = f.read()
        return self._file_pdf_content


class TestImageFile(SimpleTestCase):
    def setUp(self):
        self.data = ImageFileTestData()

    def test_valid_image(self):
        image_file = ImageFile(value=self.data.valid_image_content)

        self.assertEqual(image_file.value, self.data.valid_image_content)

    def test_image_too_large(self):
        exc = ImageFileTooLargeException

        check_raises(ImageFile.validate_image, exc)
        with self.assertRaises(exc):
            ImageFile(value=self.data.too_large_image_content)

    def test_not_supported_image_format(self):
        exc = NotSupportedImageFormatException

        check_raises(ImageFile.validate_image, exc)
        with self.assertRaises(exc):
            ImageFile(value=self.data.file_pdf_content)

    def test_str_representation(self):
        image_file = ImageFile(value=self.data.valid_image_content)

        expected_string = f"ImageFile {len(self.data.valid_image_content)} bytes"
        result = str(image_file)

        self.assertEqual(result, expected_string)

    def test_repr_representation(self):
        image_file = ImageFile(value=self.data.valid_image_content)

        expected_representation = f"ImageFile(bytes_len={len(self.data.valid_image_content)})"
        result = repr(image_file)

        self.assertEqual(result, expected_representation)
