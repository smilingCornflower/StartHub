from domain.events.project import ProjectDeletedEvent
from domain.ports.cloud_storage import AbstractCloudStorage
from domain.ports.event import AbstractEventHandler
from domain.value_objects.cloud_storage import CloudStorageDeletePayload
from loguru import logger


class ProjectDeletedEventHandler(AbstractEventHandler[ProjectDeletedEvent]):
    def __init__(
        self,
        cloud_storage: AbstractCloudStorage,
    ):
        self._cloud_storage = cloud_storage

    def handle(self, event: ProjectDeletedEvent) -> None:
        self._delete_image_files(images=event.image_paths)
        if event.plan_file_path is not None:
            self._delete_plan_file(plan_path=event.plan_file_path)

    def _delete_plan_file(self, plan_path: str) -> None:
        self._cloud_storage.delete_file(payload=CloudStorageDeletePayload(file_path=plan_path))

        logger.info("Plan was deleted successfully.")

    def _delete_image_files(self, images: list[str]) -> None:
        for img in images:
            logger.debug(f"{img=}")
            self._cloud_storage.delete_file(payload=CloudStorageDeletePayload(file_path=img))

        logger.info("All images were deleted successfully.")
