from domain.value_objects.common import Id
from domain.constants import StorageLocations


class PathProvider:
    @staticmethod
    def get_user_profile_picture_path(user_id: Id) -> str:
        return f"{StorageLocations.PROFILE_PICTURE_PATH}/{user_id.value}.jpg"

    @staticmethod
    def get_project_plan_path(project_id: Id) -> str:
        return f"{StorageLocations.PROJECT_PLAN_PATH}/{project_id.value}.pdf"

    @staticmethod
    def get_project_image_path(project_id: Id, order_number: int) -> str:
        return f"{StorageLocations.PROJECT_PHOTO_PATH}/{project_id.value}/{order_number}.jpg"
