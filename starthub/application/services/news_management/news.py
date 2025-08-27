from io import BytesIO
from pathlib import Path
from pprint import pformat
from typing import cast

from application.converters.resposne_converters.news import news_to_full_dto, news_to_short_dto
from application.dto.news import NewsFullDto, NewsImageDto, NewsShortDto
from application.ports.service import AbstractAppService
from application.ports.uow import AbstractUnitOfWork
from domain.constants import NEWS_IMAGES_MAX_AMOUNT
from domain.enums.permission import ActionEnum, ScopeEnum
from domain.events.news import NewsCreatedEvent
from domain.exceptions.cloud_storage import FileNotFoundCloudStorageException
from domain.exceptions.news import (
    NewsImageContentAndFileMismatchException,
    NewsImageMaxAmountException,
    NewsNotFoundException,
)
from domain.exceptions.permissions import (
    AddDeniedPermissionException,
    DeleteDeniedPermissionException,
    UpdateDeniedPermissionException,
)
from domain.models.news_management.news import News
from domain.models.news_management.news_image import NewsImage
from domain.models.user_management.user import User
from domain.repositories.news_management.news import NewsReadRepository
from domain.repositories.user_management.user import UserReadRepository
from domain.services.cloud_storage import StorageService
from domain.services.file import ImageService
from domain.services.news_management.news import NewsImageService, NewsService
from domain.services.permission import PermissionService
from domain.utils.path_provider import PathProvider
from domain.value_objects.cloud_storage import (
    CloudStorageCreateUrlPayload,
    CloudStorageDeletePayload,
    CloudStorageUploadPayload,
)
from domain.value_objects.common import Id, OffsetPagination
from domain.value_objects.file import Image
from domain.value_objects.filter import NewsFilter, NewsImageFilter
from domain.value_objects.news_management.news import (
    NewsContent,
    NewsCreateCommand,
    NewsCreatePayload,
    NewsGetCommand,
    NewsUpdateCommand,
    NewsUpdatePayload,
)
from domain.value_objects.news_management.news_image import NewsImageCreatePayload, NewsImageDeletePayload
from domain.value_objects.user_management.user import PermissionVo
from infrastructure.event_bus import EventBus
from loguru import logger


# TODO: Move this permission class to domain service
class NewsPermissionAppService(AbstractAppService):
    def __init__(self, permission_service: PermissionService):
        self._permission_service = permission_service

    def _check_permission_to_add_news(self, user_id: Id) -> None:
        """:raises AddDeniedPermissionException:"""
        add_news_permission: PermissionVo = self._permission_service.create_permission_vo(
            model=News, action=ActionEnum.ADD, scope=ScopeEnum.ANY
        )
        has_permission: bool = self._permission_service.has_permission(
            user_id=user_id, permission_vo=add_news_permission
        )
        if not has_permission:
            logger.error("User does not have permission to add news")
            raise AddDeniedPermissionException("User does not have permission to add news")
        logger.debug(f"User(id={user_id.value}) has permissions to add news.")
        return None

    def _check_permission_to_delete_news(self, user_id: Id) -> None:
        """:raises DeleteDeniedPermissionException:"""
        delete_news_permission: PermissionVo = self._permission_service.create_permission_vo(
            model=News, action=ActionEnum.DELETE, scope=ScopeEnum.ANY
        )
        has_permission: bool = self._permission_service.has_permission(
            user_id=user_id, permission_vo=delete_news_permission
        )
        logger.debug(f"user_id = {user_id}; has_permission = {has_permission}")
        if not has_permission:
            logger.error("User does not have permission to delete news")
            raise DeleteDeniedPermissionException("User does not have permission to delete news")

    def _check_permission_to_update_news(self, user_id: Id) -> None:
        """:raises UpdateDeniedPermissionException:"""

        change_any_news_permission: PermissionVo = self._permission_service.create_permission_vo(
            model=News, action=ActionEnum.CHANGE, scope=ScopeEnum.ANY
        )
        has_permission: bool = self._permission_service.has_permission(
            user_id=user_id, permission_vo=change_any_news_permission
        )
        if not has_permission:
            logger.error("User does not have permission to change news.")
            raise UpdateDeniedPermissionException("User does not have permission to change news.")

    def _check_permission_to_change_any_is_active_field(self, user: User) -> None:
        """:raises UpdateDeniedPermissionException:"""
        if self._permission_service.is_allowed_for_user(
            user=user, model=News, action=ActionEnum.CHANGE, scope=ScopeEnum.ANY, field=News.IS_ACTIVE_FIELD
        ):
            return None
        else:
            logger.error(f"User {user.email} doesn't have enough permission to change news is_active field.")
            raise UpdateDeniedPermissionException("User does not have permission to change news.is_active field.")


class NewsAppService(NewsPermissionAppService):
    def __init__(
        self,
        news_service: NewsService,
        news_image_service: NewsImageService,
        permission_service: PermissionService,
        image_service: ImageService,
        storage_service: StorageService,
        news_read_repository: NewsReadRepository,
        user_read_repository: UserReadRepository,
        unit_of_work: AbstractUnitOfWork,
    ):
        super().__init__(permission_service=permission_service)
        self._news_service = news_service
        self._news_image_service = news_image_service
        self._image_service = image_service
        self._storage_service = storage_service
        self._news_read_repository = news_read_repository
        self._user_read_repository = user_read_repository
        self._uow = unit_of_work

    def get_one(self, news_id: int) -> NewsFullDto:
        logger.debug("get_one()")
        news: News = self._news_read_repository.get_by_id(id_=Id(value=news_id))

        cover_url: str = self._storage_service.create_url(
            payload=CloudStorageCreateUrlPayload(file_path=cast(str, news.cover))
        )

        news_images: list[NewsImage] = self._news_image_service.get(filter_=NewsImageFilter(news_id=Id(value=news.id)))
        img_dtos: list[NewsImageDto] = list()
        for img in news_images:
            img_dtos.append(
                NewsImageDto(
                    image_name=self._news_image_service.extract_image_name(news_image=img),
                    image_url=self._storage_service.create_url(CloudStorageCreateUrlPayload(file_path=img.image)),
                )
            )
        news_dto: NewsFullDto = news_to_full_dto(news, cover_url=cover_url, news_image_dtos=img_dtos)

        return news_dto

    def get_many(self, pagination: OffsetPagination, command: NewsGetCommand) -> list[NewsShortDto]:
        logger.debug("get_many()")

        news_lst: list[News] = self._news_read_repository.get_all(
            pagination=pagination,
            filter_=NewsFilter(
                published_at_start=command.published_at_start,
                published_at_end=command.published_at_end,
                order_by_lst=["-published_at"],
            ),
        )
        logger.debug(f"Found {len(news_lst)} news.")

        cover_urls: list[str] = [
            self._storage_service.create_url(payload=CloudStorageCreateUrlPayload(file_path=cast(str, i.cover)))
            for i in news_lst
        ]

        return [news_to_short_dto(news, cover) for news, cover in zip(news_lst, cover_urls)]

    def _update_cover(self, news_id: Id, cover: Image) -> None:
        cover_jpg: BytesIO = self._image_service.convert_to_jpg(file_obj=BytesIO(cover.file.value))
        cover_path: str = PathProvider.get_news_cover_path(news_id=news_id)

        self._storage_service.upload_file(CloudStorageUploadPayload(file_data=cover_jpg.read(), file_path=cover_path))
        logger.debug(f"cover uploaded by the path: {cover_path}")

        self._news_service.update(payload=NewsUpdatePayload(news_id=news_id, cover_path=cover_path))
        logger.debug("cover field updated in news")

    def create(
        self,
        user_id: Id,
        news_create_command: NewsCreateCommand,
    ) -> int:
        """
        :raises MissingRequiredFieldException:
        :raises MissingFileExcpetion: If an image provided in the content but lacks in files
        :raises NotSupportedImageFormatException:
        :raises ValidationError: if fields has invalid data types (pydantic.ValidationError)
        """
        self._check_permission_to_add_news(user_id=user_id)
        self._validate_images_amount_in_content(content=news_create_command.content)
        self._validate_image_files_used(content=news_create_command.content, images=news_create_command.images)
        self._validate_images_in_content_exist_in_files_or_database(
            content=news_create_command.content, images=news_create_command.images
        )

        new_content, id_map = self._news_service.replace_filenames_with_id(md=news_create_command.content.value)
        logger.debug(f"id_map = {pformat(id_map)}")
        logger.debug(f"news_content = {pformat(new_content)}")

        with self._uow:
            news: News = self._news_service.create(
                self._convert_create_command_to_payload(
                    command=news_create_command, new_content=new_content, author_id=user_id
                )
            )
            event = NewsCreatedEvent(news_id=Id(value=news.id), tags=news_create_command.tags)
            EventBus().publish(event)

            # upload_file cover
            self._update_cover(cover=news_create_command.cover, news_id=Id(value=news.id))

            # upload_file images
            for img in news_create_command.images:
                self.upload_image(image=img, news_id=Id(value=news.id), id_map=id_map)
            logger.info("All images uploaded successfully.")
        return news.id

    def _convert_create_command_to_payload(
        self, command: NewsCreateCommand, new_content: str, author_id: Id
    ) -> NewsCreatePayload:
        return NewsCreatePayload(
            title=command.title,
            subtitle=command.subtitle,
            content=NewsContent(value=new_content),
            author_id=author_id,
        )

    def _validate_images_amount_in_content(self, content: NewsContent) -> None:
        """
        Validates that the number of images in the content does not exceed the allowed limit.
        :raises NewsImagesMaxAmountException: if the number of images exceeds NEWS_IMAGES_MAX_AMOUNT
        """
        logger.debug("_validate_images_amount_in_content()")
        if self._news_service.get_images_amount_in_content(content=content) > NEWS_IMAGES_MAX_AMOUNT:
            logger.exception(f"News images max limit is {NEWS_IMAGES_MAX_AMOUNT}.")
            raise NewsImageMaxAmountException(f"News images max limit is {NEWS_IMAGES_MAX_AMOUNT}.")

    def _validate_image_files_used(self, content: NewsContent, images: list[Image] | None) -> None:
        """
        Validates that all provided image files are referenced in the content.
        :raises NewsImageContentAndFileMismatchException: if any image file is not used in the content
        """
        logger.debug("_validate_image_files_used()")
        all_image_names_in_content: list[str] = self._news_service.get_all_image_names_from_content(content=content)
        if images is not None:
            for i in images:
                if i.name not in all_image_names_in_content:
                    logger.exception(
                        f"Each image file must be referenced in the content. Missing reference for: {i.name}"
                    )
                    raise NewsImageContentAndFileMismatchException(
                        f"Each image file must be referenced in the content. Missing reference for: {i.name}"
                    )

        logger.info("All images in files are used in content")

    def _validate_images_in_content_exist_in_files_or_database(
        self, content: NewsContent, images: list[Image] | None, news_id: Id | None = None
    ) -> None:
        """
        Validates that all images referenced in the content exist either in the database or in the provided files.
        If an image is missing in both, an exception is raised.
        When `news_id` is None, only the files are checked because there are no database records.

        :raises NewsImageContentAndFileMismatchException: If a content image is missing in both database and files
        """
        logger.debug("_validate_images_in_content_exist_in_files_or_database()")

        content_image_names: list[str] = self._news_service.get_all_image_names_from_content(content=content)
        logger.debug(f"content_image_names: {pformat(content_image_names)}")

        news_image_names_in_database = list()
        if news_id is not None:
            news_images_in_database: list[NewsImage] = self._news_image_service.get(
                filter_=NewsImageFilter(news_id=news_id)
            )
            news_image_names_in_database = [Path(i.image).name for i in news_images_in_database]
            logger.debug(f"news_image_names_in_database: {pformat(news_image_names_in_database)}")

        image_names_in_files: list[str] = [i.name for i in images] if images else list()
        logger.debug(f"image_names_in_files: {pformat(image_names_in_files)}")

        for img in content_image_names:
            if img not in news_image_names_in_database and img not in image_names_in_files:
                logger.debug(f"{content_image_names=}")
                logger.debug(f"{image_names_in_files=}")
                logger.debug(f"{news_image_names_in_database=}")

                logger.exception(
                    f"Content references image '{img}', but it's missing in both uploaded files and existing records."
                )
                raise NewsImageContentAndFileMismatchException(
                    f"Content references image '{img}', but it's missing in both uploaded files and existing records."
                )
        logger.debug("All images in content exist in files or in database")

    def _get_images_to_remove(self, content: NewsContent, news_id: Id) -> list[str]:
        """
        Get list of image paths that should be removed from storage and database.

        Compares images currently stored in database with images referenced in new content.
        Returns paths of images that exist in database but are no longer referenced in content.

        Example:
            Previous content had img1, img2, img3
            New content has only img1, img2 and img4
            Returns path for img3 to be removed

        Args:
            content: New news content with image references
            news_id: News identifier

        Returns:
            List of image file paths to remove from storage and database
        """
        logger.debug("_get_images_to_remove()")

        command_image_names: list[str] = self._news_service.get_all_image_names_from_content(content)
        news_images_in_database: list[NewsImage] = self._news_image_service.get(
            filter_=NewsImageFilter(news_id=news_id)
        )

        result: list[str] = list()

        for img in news_images_in_database:
            if Path(img.image).name not in command_image_names:
                result.append(img.image)
        return result

    def update(
        self,
        update_command: NewsUpdateCommand,
        news_id: Id,
        user_id: Id,
    ) -> None:
        """
        :raises UpdateDeniedPermissionException:
        :raises NewsImagesMaxAmountException:
        :raises ValidationError:
        :raises NewsImageContentAndFileMismatchException:
        """
        logger.info("Started news update()")
        self._check_permission_to_update_news(user_id=user_id)

        with self._uow:
            if update_command.title or update_command.subtitle:
                self._news_service.update(
                    payload=NewsUpdatePayload(
                        news_id=news_id, title=update_command.title, subtitle=update_command.subtitle
                    )
                )

            if update_command.cover is not None:
                self._update_cover(cover=update_command.cover, news_id=news_id)

            if update_command.content:
                self._validate_images_amount_in_content(content=update_command.content)
                self._validate_image_files_used(content=update_command.content, images=update_command.images)
                self._validate_images_in_content_exist_in_files_or_database(
                    content=update_command.content, news_id=news_id, images=update_command.images
                )

                image_names_to_remove: list[str] = self._get_images_to_remove(
                    content=update_command.content, news_id=news_id
                )
                logger.info(f"{image_names_to_remove=}")

                for img in image_names_to_remove:
                    try:
                        self._storage_service.delete_file(payload=CloudStorageDeletePayload(file_path=img))
                    except FileNotFoundCloudStorageException:
                        logger.warning("File does not exists.")

                    self._news_image_service.delete(data=NewsImageDeletePayload(file_name=img))

                new_content, images_id_map = self._news_service.replace_filenames_with_id(
                    md=update_command.content.value,
                    filenames=[i.name for i in update_command.images] if update_command.images else None,
                )
                if update_command.images:
                    for image in update_command.images:
                        self.upload_image(image=image, news_id=news_id, id_map=images_id_map)

                    self._news_service.update(
                        payload=NewsUpdatePayload(news_id=news_id, content=NewsContent(value=new_content))
                    )
                else:  # It means no images to remove or upload_file, then updating only text part of the content
                    self._news_service.update(
                        payload=NewsUpdatePayload(news_id=news_id, content=update_command.content)
                    )

    def upload_image(self, image: Image, news_id: Id, id_map: dict[str, str]) -> None:
        logger.info(f"Uploading image {image}")
        logger.debug(f"converting image = {image}")
        jpg_obj: BytesIO = self._image_service.convert_to_jpg(file_obj=BytesIO(image.file.value))
        img_path: str = PathProvider.get_news_image_path(news_id, image_name=id_map[image.name])
        self._storage_service.upload_file(CloudStorageUploadPayload(file_data=jpg_obj.read(), file_path=img_path))
        logger.debug(f"{img_path} uploaded successfully.")

        news_image: NewsImage = self._news_image_service.create(NewsImageCreatePayload(news_id=news_id, image=img_path))
        logger.debug(f"{news_image} created.")

    def delete(self, news_id: int, user_id: int) -> None:
        """:raises DeleteDeniedPermissionException:"""
        self._check_permission_to_delete_news(user_id=Id(value=user_id))
        try:
            news = self._news_read_repository.get_by_id(id_=Id(value=news_id))

            self._storage_service.delete_file(payload=CloudStorageDeletePayload(file_path=cast(str, news.cover)))
            logger.info(f"Cover deleted: {news.cover}")

            for img in self._news_image_service.get(filter_=NewsImageFilter(news_id=Id(value=news_id))):
                self._storage_service.delete_file(payload=CloudStorageDeletePayload(file_path=img.image))
                logger.info(f"Image deleted: {img.image}")

        except NewsNotFoundException:
            logger.exception("news not found, skipping this exception")

        self._news_service.delete_by_id(Id(value=news_id))

        logger.debug("News deleted.")

    def activate(self, news_id: Id, user_id: Id) -> None:
        user = self._user_read_repository.get_by_id(id_=user_id)
        self._check_permission_to_change_any_is_active_field(user=user)
        self._news_service.activate(news_id=news_id)

    def deactivate(self, news_id: Id, user_id: Id) -> None:
        user = self._user_read_repository.get_by_id(id_=user_id)
        self._check_permission_to_change_any_is_active_field(user=user)
        self._news_service.deactivate(news_id=news_id)
