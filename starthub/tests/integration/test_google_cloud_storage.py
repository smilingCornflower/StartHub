import requests
from django.test import SimpleTestCase, tag
from domain.value_objects.cloud_storage import (
    CloudStorageCreateUrlPayload,
    CloudStorageDeletePayload,
    CloudStorageUploadPayload,
)
from filetype import guess
from infrastructure.cloud_storages.google import GoogleCloudStorageFactory
from tests.common.check_raises import check_raises_in_docs
from tests.common.constants import TEST_FILES_PATH


@tag("slow")
class TestGoogleCloudStorage(SimpleTestCase):
    def setUp(self):
        self.storage = GoogleCloudStorageFactory.create()
        self.upload_path = "tests/integration/image.jpg"
        self.image_path = TEST_FILES_PATH / "img.jpg"
        self.image_mime = "image/jpeg"
        with open(self.image_path, mode="rb") as f:
            self.image_data = f.read()

    def test_update_file(self):
        before = self.storage.check_url_exists(url=self.upload_path)
        uploaded_path = self.storage.upload_file(
            payload=CloudStorageUploadPayload(file_data=self.image_data, file_path=self.upload_path)
        )
        after = self.storage.check_url_exists(url=uploaded_path)

        self.assertEqual(uploaded_path, self.upload_path)
        self.assertFalse(before)
        self.assertTrue(after)

        self.storage.delete_file(payload=CloudStorageDeletePayload(file_path=self.upload_path))

    def test_delete_file(self):
        self.storage.upload_file(
            payload=CloudStorageUploadPayload(file_data=self.image_data, file_path=self.upload_path)
        )
        before = self.storage.check_url_exists(url=self.upload_path)
        self.storage.delete_file(payload=CloudStorageDeletePayload(file_path=self.upload_path))
        after = self.storage.check_url_exists(url=self.upload_path)

        self.assertTrue(before)
        self.assertFalse(after)

    def create_url_test(self):
        self.storage.upload_file(
            payload=CloudStorageUploadPayload(file_data=self.image_data, file_path=self.upload_path)
        )
        url = self.storage.create_url(payload=CloudStorageCreateUrlPayload(file_path=self.upload_path))

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(guess(response.content).mime, self.image_mime)
        self.storage.delete_file(payload=CloudStorageDeletePayload(file_path=self.upload_path))

    def test_create_url(self):
        self.create_url_test()

    def test_create_url_or_none(self):
        self.create_url_test()

    def test_create_url_for_not_existing_file(self):
        from google.cloud.exceptions import NotFound

        with self.assertRaises(NotFound):
            self.storage.create_url(payload=CloudStorageCreateUrlPayload(file_path="not-existing-file.jpg"))
        check_raises_in_docs(self.storage.create_url, NotFound)

    def test_create_url_or_none_for_not_existing_file(self):
        result = self.storage.create_url_or_none(
            payload=CloudStorageCreateUrlPayload(file_path="not-existing-file.jpg")
        )
        self.assertIsNone(result)

    def test_check_url_exists(self):
        before = self.storage.check_url_exists(url=self.upload_path)

        self.storage.upload_file(
            payload=CloudStorageUploadPayload(file_data=self.image_data, file_path=self.upload_path)
        )
        after = self.storage.check_url_exists(url=self.upload_path)
        self.assertFalse(before)
        self.assertTrue(after)
        self.storage.delete_file(payload=CloudStorageDeletePayload(file_path=self.upload_path))
