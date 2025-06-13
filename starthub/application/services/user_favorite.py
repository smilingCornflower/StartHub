from application.converters.resposne_converters.user import user_favorite_to_dto
from application.dto.user import UserFavoriteDto
from application.ports.service import AbstractAppService
from domain.models.user_favorite import UserFavorite
from domain.services.user_favorite import UserFavoriteService
from domain.value_objects.common import Id
from domain.value_objects.user_favorite import UserFavoriteCreatePayload
from loguru import logger


class UserFavoriteAppService(AbstractAppService):
    def __init__(self, user_favorite_service: UserFavoriteService):
        self._user_favorite_service = user_favorite_service

    def add_favorite(self, user_id: int, project_id: int) -> None:
        logger.info(f"Adding favorite: user_id={user_id}, project_id={project_id}")

        self._user_favorite_service.add_favorite(
            UserFavoriteCreatePayload(user_id=Id(value=user_id), project_id=Id(value=project_id))
        )

    def get_user_favorites(self, user_id: int) -> list[UserFavoriteDto]:
        logger.info(f"Getting favorites for user_id={user_id}")

        user_favorites: list[UserFavorite] = self._user_favorite_service.get_user_favorites(Id(value=user_id))
        return [user_favorite_to_dto(i) for i in user_favorites]

    def delete_by_association_ids(self, user_id: int, project_id: int) -> None:
        logger.info(f"Deleting favorite: user_id={user_id}, project_id={project_id}")

        self._user_favorite_service.delete_by_association_ids(Id(value=user_id), Id(value=project_id))
