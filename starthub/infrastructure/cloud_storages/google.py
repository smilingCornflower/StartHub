from datetime import timedelta
from io import BytesIO
from typing import cast

from config import settings
from domain.ports.cloud_storage import AbstractCloudStorage
from domain.value_objects.cloud_storage import (
    CloudStorageCreateUrlPayload,
    CloudStorageDeletePayload,
    CloudStorageUploadPayload,
)
from google.cloud.exceptions import GoogleCloudError, NotFound
from google.cloud.storage import Bucket, Client
from google.cloud.storage.blob import Blob
from loguru import logger


class GoogleCloudStorage(AbstractCloudStorage):
    def __init__(self, bucket_name: str):
        self._bucket_name = bucket_name
        self._client: Client | None = None
        self._bucket: Bucket | None = None

    @property
    def client(self) -> Client:
        if self._client is None:
            self._client = Client()
            logger.info("Google cloud storage client initialized.")
        return self._client

    @property
    def bucket(self) -> Bucket:
        if self._bucket is None:
            try:
                self._bucket = self.client.get_bucket(self._bucket_name)
                logger.info("Bucket initialized.")
            except GoogleCloudError as err:
                logger.critical(f"Error during connection to bucket. Error: {err}")
                raise err
        return self._bucket

    def upload_file(self, payload: CloudStorageUploadPayload) -> str:
        """Upload a file to Google Cloud Storage bucket.

        :param payload: Upload payload containing file data and destination path
        :return: Full path to the uploaded file in GCS
        :raises GoogleCloudError: If upload operation fails
        """
        logger.warning("Started uploading a file into the bucket.")

        blob: Blob = self.bucket.blob(blob_name=payload.file_path)
        logger.debug(f"Blob: {blob}")
        try:
            blob.upload_from_file(file_obj=BytesIO(payload.file_data), rewind=True)
            logger.info("File uploaded into the bucket.")
            return cast(str, blob.name)
        except GoogleCloudError as e:
            logger.error(f"Cloud error during uploading: {e}")
            raise e

    def delete_file(self, payload: CloudStorageDeletePayload) -> None:
        """Delete a file from Google Cloud Storage bucket.

        :param payload: Delete payload containing file path to delete
        :raises NotFound: If specified file doesn't exist in bucket
        :raises GoogleCloudError: If delete operation fails
        """
        logger.warning(f"Started deleting blob: {payload.file_path}.")

        blob: Blob = self.bucket.blob(blob_name=payload.file_path)
        try:
            blob.delete()
            logger.info("Finished deleting blob")
        except NotFound:
            logger.error(f"Blob {payload.file_path} not found in bucket.")
            raise
        except GoogleCloudError as e:
            logger.error(f"Google Cloud error during deleting blob {payload.file_path}: {e}")
            raise e

    def create_url(self, payload: CloudStorageCreateUrlPayload) -> str:
        """Generate a signed URL for accessing a file in Google Cloud Storage.

        :param payload: URL creation payload containing file path
        :return: Signed URL for temporary access to the file
        :raises GoogleCloudError: If URL generation fails
        """
        blob: Blob = self.bucket.blob(blob_name=payload.file_path)
        try:
            return cast(str, blob.generate_signed_url(version="v4", expiration=timedelta(minutes=15)))
        except GoogleCloudError as e:
            logger.error(f"Google Cloud error during generating url for {payload.file_path}: {e}")
            raise e


google_cloud_storage = GoogleCloudStorage(bucket_name=settings.GOOGLE_CLOUD_BUCKET_NAME)
