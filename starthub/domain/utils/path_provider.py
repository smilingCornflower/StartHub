from uuid import uuid4

from config.settings import MODE
from domain.ports.service import AbstractDomainService
from domain.value_objects.common import Id


class StorageLocations:
    PROFILE_PICTURE_PATH = MODE + "/profile_pictures"  # + /user_id.jpg
    PROJECT_PHOTO_PATH = MODE + "/projects/photos"  # + /photo_order.jpg
    NEWS_IMAGE_PATH = MODE + "/news"  # + news_id/image_uuid.jpg


class PathProvider(AbstractDomainService):
    @staticmethod
    def get_user_profile_picture_path(user_id: Id) -> str:
        return f"{StorageLocations.PROFILE_PICTURE_PATH}/{user_id.value}.jpg"

    @staticmethod
    def get_project_plan_path() -> str:
        return f"{MODE}/projects/plans/{uuid4()}.pdf"

    @staticmethod
    def get_project_image_path(project_id: Id) -> str:
        return f"{StorageLocations.PROJECT_PHOTO_PATH}/{project_id.value}/{str(uuid4())}.jpg"

    @staticmethod
    def get_news_image_path(news_id: Id, image_name: str) -> str:
        return f"{StorageLocations.NEWS_IMAGE_PATH}/{news_id.value}/{image_name}"

    @staticmethod
    def get_news_cover_path(news_id: Id) -> str:
        return f"{StorageLocations.NEWS_IMAGE_PATH}/{news_id.value}/{str(uuid4())}.jpg"

    @staticmethod
    def get_project_file_path(project_id: Id, file_extension: str) -> str:
        """
        prod/projects/files/123/a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg
        test/projects/files/456/f9e8d7c6-b5a4-3210-9876-543210fedcba.pdf
        """
        return f"{MODE}/projects/files/{project_id.value}/{str(uuid4())}.{file_extension}"

    @staticmethod
    def get_project_media_path(project_id: Id, file_extension: str) -> str:
        """
        prod/projects/media/123/a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg
        test/projects/media/456/f9e8d7c6-b5a4-3210-9876-543210fedcba.pdf
        """
        return f"{MODE}/projects/media/{project_id.value}/{str(uuid4())}.{file_extension}"
