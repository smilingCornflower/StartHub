from dataclasses import dataclass
from io import BytesIO

from django.test import SimpleTestCase
from domain.constants import IMAGE_MAX_SIZE_IN_BYTES, MEGABYTE, VIDEO_MAX_SIZE_IN_BYTES
from domain.exceptions.file import (
    ImageFileTooLargeException,
    UnsupportedFileExtensionException,
    VideoFileTooLargeException,
)
from domain.value_objects.project.media import MediaFile
from tests.common.constants import TEST_FILES_PATH
from tests.utils import check_raises


@dataclass
class MediaFileTestData:
    _valid_image_content = None
    _too_large_image_content = None
    _valid_video_content = None
    _too_large_video_content = None
    _unsupported_file_content = None
    valid_image_file_extension = "jpg"

    @property
    def valid_image_content(self):
        if self._valid_image_content is None:
            with open(TEST_FILES_PATH / "img.jpg", "rb") as f:
                self._valid_image_content = f.read()
        return self._valid_image_content

    @property
    def too_large_image_content(self):
        if self._too_large_image_content is None:
            with open(TEST_FILES_PATH / "large_img.png", "rb") as f:
                self._too_large_image_content = f.read()
        return self._too_large_image_content

    @property
    def valid_video_content(self):
        if self._valid_video_content is None:
            with open(TEST_FILES_PATH / "video.mp4", "rb") as f:
                self._valid_video_content = f.read()
        return self._valid_video_content

    @property
    def too_large_video_content(self):
        if self._too_large_video_content is None:
            self._too_large_video_content = self.valid_video_content + b"0" * (VIDEO_MAX_SIZE_IN_BYTES + 1)
        return self._too_large_video_content

    @property
    def unsupported_file_content(self):
        if self._unsupported_file_content is None:
            with open(TEST_FILES_PATH / "file.pdf", "rb") as f:
                self._unsupported_file_content = f.read()
        return self._unsupported_file_content


class TestMediaFile(SimpleTestCase):
    def setUp(self):
        self.data = MediaFileTestData()

    def test_valid_image_file(self):
        media_file = MediaFile(value=self.data.valid_image_content)
        self.assertEqual(media_file.value, self.data.valid_image_content)

    def test_image_file_too_large(self):
        exc = ImageFileTooLargeException
        check_raises(MediaFile.validate_file_size, exc)
        with self.assertRaises(exc):
            MediaFile(value=self.data.too_large_image_content)

    def test_valid_video_file(self):
        media_file = MediaFile(value=self.data.valid_video_content)
        self.assertEqual(media_file.value, self.data.valid_video_content)

    def test_video_file_too_large(self):
        exc = VideoFileTooLargeException
        check_raises(MediaFile.validate_file_size, exc)
        with self.assertRaises(exc):
            MediaFile(value=self.data.too_large_video_content)

    def test_unsupported_file_extension(self):
        exc = UnsupportedFileExtensionException
        check_raises(MediaFile._validate_file_extesnsion, exc)
        with self.assertRaises(exc):
            MediaFile(value=self.data.unsupported_file_content)

    def test_get_file_extension(self):
        media = MediaFile(value=self.data.valid_image_content)
        self.assertEqual(media.file_extension, self.data.valid_image_file_extension)
