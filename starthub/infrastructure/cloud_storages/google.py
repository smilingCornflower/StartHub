from datetime import timedelta
from typing import BinaryIO, cast

from domain.ports.cloud_storage import AbstractCloudStorage
from google.cloud.exceptions import GoogleCloudError, NotFound
from google.cloud.storage import Bucket, Client
from google.cloud.storage.blob import Blob
from loguru import logger


class GoogleCloudStorage(AbstractCloudStorage):
    def __init__(self, bucket_name: str):
        self._client = Client()
        logger.info("Google cloud storage client initialized.")
        try:
            self._bucket: Bucket = self._client.get_bucket(bucket_or_name=bucket_name)
            logger.info("Bucket initialized.")
        except GoogleCloudError as err:
            logger.critical(f"Error during connection to bucket. Error: {err}")
            raise err

    def upload_file(self, file_obj: BinaryIO, file_name: str) -> str:
        """
        Upload a file to bucket and return the blob's name.

        :param file_obj: File object opened in binary mode.
        :param file_name: Name of the blob in bucket.
        :return: Name of the uploaded blob.
        :raises GoogleCloudError:
        """
        logger.warning("Started uploading a file into the bucket.")

        blob: Blob = self._bucket.blob(blob_name=file_name)
        logger.debug(f"Blob: {blob}")
        try:
            blob.upload_from_file(file_obj=file_obj, rewind=True)
            logger.info("File uploaded into the bucket.")
            return cast(str, blob.name)
        except GoogleCloudError as e:
            logger.error(f"Cloud error during uploading: {e}")
            raise e

    def delete_file(self, file_name: str) -> None:
        """
        Delete a file from bucket by its blob name.

        :param file_name: Name of the blob in bucket to delete.
        :raises: google.cloud.exceptions.NotFound:
        :raises: GoogleCloudError:
        """
        logger.warning(f"Started deleting blob: {file_name}.")

        blob: Blob = self._bucket.blob(blob_name=file_name)
        try:
            blob.delete()
            logger.info("Finished deleting blob")
        except NotFound:
            logger.error(f"Blob {file_name} not found in bucket.")
        except GoogleCloudError as e:
            logger.error(f"Google Cloud error during deleting blob {file_name}: {e}")
            raise e

    def create_url(self, file_name: str) -> str:
        """
        Generate a signed URL for a Google Cloud Storage blob.

        :param file_name: the name of the blob for which to generate the URL.
        :return: the signed URL for accessing the blob.
        :raises GoogleCloudError:
        """
        blob: Blob = self._bucket.blob(blob_name=file_name)
        try:
            return cast(str, blob.generate_signed_url(version="v4", expiration=timedelta(minutes=15)))
        except GoogleCloudError as e:
            logger.error(f"Google Cloud error during generating url for {file_name}: {e}")
            raise e
