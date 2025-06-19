from uuid import uuid4

from domain.constants import StorageLocations
from domain.ports.service import AbstractDomainService
from domain.value_objects.common import Id


class PathProvider(AbstractDomainService):
    @staticmethod
    def get_user_profile_picture_path(user_id: Id) -> str:
        return f"{StorageLocations.PROFILE_PICTURE_PATH}/{user_id.value}.jpg"

    @staticmethod
    def get_project_plan_path(project_id: Id) -> str:
        return f"{StorageLocations.PROJECT_PLAN_PATH}/{project_id.value}.pdf"

    @staticmethod
    def get_project_image_path(project_id: Id) -> str:
        return f"{StorageLocations.PROJECT_PHOTO_PATH}/{project_id.value}/{str(uuid4())}.jpg"

    @staticmethod
    def get_news_image_path() -> str:
        return f"{StorageLocations.NEWS_IMAGE_PATH}/{str(uuid4())}.jpg"
