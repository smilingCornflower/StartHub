from io import BytesIO

from domain.models.news import News
from domain.ports.cloud_storage import AbstractCloudStorage
from domain.ports.service import AbstractDomainService
from domain.repositories.news import NewsReadRepository, NewsWriteRepository
from domain.services.file import ImageService
from domain.utils.path_provider import PathProvider
from domain.value_objects.cloud_storage import CloudStorageUploadPayload
from domain.value_objects.common import Id
from domain.value_objects.filter import NewsFilter
from domain.value_objects.news import NewsCreateCommand, NewsCreatePayload, NewsImageUploadCommand
from loguru import logger


class NewsService(AbstractDomainService):
    def __init__(
        self,
        news_read_repository: NewsReadRepository,
        news_write_repository: NewsWriteRepository,
        cloud_storage: AbstractCloudStorage,
        image_service: ImageService,
    ):
        self._news_read_repository = news_read_repository
        self._news_write_repository = news_write_repository
        self._cloud_storage = cloud_storage
        self._image_service = image_service

    def get_one(self, id_: Id) -> News:
        return self._news_read_repository.get_by_id(id_=id_)

    def get_many(self, filter_: NewsFilter):
        news: list[News] = self._news_read_repository.get_all(filter_=filter_)
        logger.debug(f"Found {len(news)} news")
        return news

    def create(self, command: NewsCreateCommand) -> News:
        image_path: str = self.upload_news_image(NewsImageUploadCommand(image=command.image))

        news: News = self._news_write_repository.create(
            NewsCreatePayload(
                title=command.title,
                content=command.content,
                author_id=command.author_id,
                image_url=image_path,
            )
        )
        logger.info(f"News posted successfully with id = {news.id}")
        return news

    def upload_news_image(self, command: NewsImageUploadCommand) -> str:
        convert_image_to_jpg: BytesIO = self._image_service.convert_to_jpg(BytesIO(command.image.value))
        logger.info("The image converted to jpg successfully.")

        file_path: str = PathProvider.get_news_image_path()
        logger.debug(f"file_path: {file_path}")

        uploaded_path: str = self._cloud_storage.upload_file(
            CloudStorageUploadPayload(file_data=convert_image_to_jpg.getvalue(), file_path=file_path)
        )
        logger.debug(f"File uploaded into the {uploaded_path}.")
        return uploaded_path
