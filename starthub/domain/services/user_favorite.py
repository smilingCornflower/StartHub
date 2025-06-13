from domain.exceptions.user_favorite import UserFavoriteAlreadyExistsException
from domain.models.user_favorite import UserFavorite
from domain.repositories.project_management import ProjectReadRepository
from domain.repositories.user import UserReadRepository
from domain.repositories.user_favorite import UserFavoriteReadRepository, UserFavoriteWriteRepository
from domain.value_objects.common import Id
from domain.value_objects.filter import UserFavoriteFilter
from domain.value_objects.user_favorite import UserFavoriteCreatePayload
from loguru import logger


class UserFavoriteService:
    def __init__(
        self,
        user_favorite_read_repository: UserFavoriteReadRepository,
        user_favorite_write_repository: UserFavoriteWriteRepository,
        user_read_repository: UserReadRepository,
        project_read_repository: ProjectReadRepository,
    ):
        self._user_favorite_read_repository = user_favorite_read_repository
        self._user_favorite_write_repository = user_favorite_write_repository
        self._user_read_repository = user_read_repository
        self._project_read_repository = project_read_repository

    def add_favorite(self, payload: UserFavoriteCreatePayload) -> UserFavorite:
        """
        :raises UserNotFoundException:
        :raises ProjectNotFoundException:
        :raises UserFavoriteNotFoundException:
        """

        self._user_read_repository.get_by_id(payload.user_id)
        self._project_read_repository.get_by_id(payload.project_id)
        search_result: list[UserFavorite] = self._user_favorite_read_repository.get_all(
            UserFavoriteFilter(user_id=payload.user_id, project_id=payload.project_id)
        )
        if search_result:
            logger.warning(
                f"UserFavorite already exists for user_id={payload.user_id.value}, project_id={payload.project_id.value}"
            )
            raise UserFavoriteAlreadyExistsException(
                f"UserFavorite with (user_id={payload.user_id.value}, project_id={payload.project_id.value}) already exists."
            )

        logger.debug("Creating UserFavorite")
        return self._user_favorite_write_repository.create(payload)

    def get_user_favorites(self, user_id: Id) -> list[UserFavorite]:
        """:raises UserNotFoundException:"""

        self._user_read_repository.get_by_id(user_id)
        user_favorites: list[UserFavorite] = self._user_favorite_read_repository.get_all(
            UserFavoriteFilter(user_id=user_id)
        )
        logger.debug(f"Found {len(user_favorites)} favorites with user_id = {user_id.value}")

        return user_favorites

    def delete_by_association_ids(self, user_id: Id, project_id: Id) -> None:
        """:raises UserFavoriteNotFoundException:"""
        self._user_favorite_write_repository.delete_by_association_ids(user_id, project_id)
