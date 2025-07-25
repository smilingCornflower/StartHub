from loguru import logger

from application.converters.resposne_converters.project import projects_to_dtos
from application.converters.resposne_converters.user import user_favorite_to_dto
from application.dto.project import ProjectDto
from application.dto.user import UserFavoriteDto
from application.ports.service import AbstractAppService
from domain.models import Project
from domain.models.user_favorite import UserFavorite
from domain.repositories.project_management import ProjectReadRepository
from domain.services.user_management import UserFavoriteService
from domain.value_objects.common import Id
from domain.value_objects.filter import ProjectFilter
from domain.value_objects.user_favorite import UserFavoriteCreatePayload


class UserFavoriteAppService(AbstractAppService):
    def __init__(
        self,
        user_favorite_service: UserFavoriteService,
        project_read_repository: ProjectReadRepository,
    ):
        self._user_favorite_service = user_favorite_service
        self._project_read_repository = project_read_repository

    def add_favorite(self, user_id: int, project_id: int) -> None:
        """
        :raises UserNotFoundException:
        :raises ProjectNotFoundException:
        :raises UserFavoriteAlreadyExistsException:
        """
        logger.info(f"Adding favorite: user_id={user_id}, project_id={project_id}")

        self._user_favorite_service.add_favorite(
            UserFavoriteCreatePayload(user_id=Id(value=user_id), project_id=Id(value=project_id))
        )

    def get_user_favorites(self, user_id: int) -> list[UserFavoriteDto]:
        """
        :raises UserNotFoundException:
        """
        logger.info(f"Getting favorites for user_id={user_id}")

        user_favorites: list[UserFavorite] = self._user_favorite_service.get_user_favorites(Id(value=user_id))
        return [user_favorite_to_dto(i) for i in user_favorites]

    def get_user_favorite_projects(self, user_id: int) -> list[ProjectDto]:
        """
        :raises UserNotFoundException:
        """
        user_favorites: list[UserFavorite] = self._user_favorite_service.get_user_favorites(Id(value=user_id))
        project_id_list: list[Id] = [Id(value=i.project_id) for i in user_favorites]
        favorite_projects: list[Project] = self._project_read_repository.get_all(
            filter_=ProjectFilter(id_list=project_id_list)
        )

        return projects_to_dtos(favorite_projects)

    def delete_by_association_ids(self, user_id: int, project_id: int) -> None:
        """:raises UserFavoriteNotFoundException:"""
        logger.info(f"Deleting favorite: user_id={user_id}, project_id={project_id}")

        self._user_favorite_service.delete_by_association_ids(Id(value=user_id), Id(value=project_id))
