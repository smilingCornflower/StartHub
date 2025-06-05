from domain.ports.cloud_storage import AbstractCloudStorage


class CloudService:
    def __init__(self, cloud_storage: AbstractCloudStorage):
        self._cloud_storage = cloud_storage

    def upload_file(self) -> str:
        raise NotImplementedError("The method upload_file() is not implemented yet.")

    def delete_file(self) -> None:
        raise NotImplementedError("The method delete_file() is not implemented yet.")

    def create_url(self) -> str:
        raise NotImplementedError("The method update_file() is not implemented yet.")
