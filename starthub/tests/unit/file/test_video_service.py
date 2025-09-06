from django.test import SimpleTestCase, tag
from domain.services.file import VideoService
from loguru import logger
from msgpack.fallback import BytesIO
from tests.common.constants import TEST_FILES_PATH


@tag("slow")
class TestVideoService(SimpleTestCase):
    def test_compress_video(self):
        with open(TEST_FILES_PATH / "video_4k.mp4", mode="rb") as video:
            video_data = video.read()
            size_before = len(video_data)
            logger.debug(f"Size before: {size_before}")
        compressed = VideoService.compress_video(file_obj=BytesIO(video_data))
        size_after = len(compressed.read())
        logger.debug(f"Size after: {size_after}")

        self.assertTrue(size_after < size_before)
