from domain.exceptions.user_favorite import UserFavoriteNotFoundException
from domain.models.user_favorite import UserFavorite
from domain.repositories.user_favorite import UserFavoriteReadRepository, UserFavoriteWriteRepository
from domain.value_objects.common import Id
from domain.value_objects.filter import UserFavoriteFilter
from domain.value_objects.user_favorite import UserFavoriteCreatePayload, UserFavoriteUpdatePayload


class DjUserFavoriteReadRepository(UserFavoriteReadRepository):
    def get_by_id(self, id_: Id) -> UserFavorite:
        user_favorite: UserFavorite | None = UserFavorite.objects.filter(id=id_.value).first()
        if user_favorite is None:
            raise UserFavoriteNotFoundException(f"UserFavorite with id = {id_.value} not found.")
        return user_favorite

    def get_all(self, filter_: UserFavoriteFilter) -> list[UserFavorite]:
        queryset = UserFavorite.objects.all()
        if filter_.user_id:
            queryset = queryset.filter(user_id=filter_.user_id.value)
        if filter_.project_id:
            queryset = queryset.filter(project_id=filter_.project_id.value)
        return list(queryset.distinct())

    def get_by_association_ids(self, user_id: Id, project_id: Id) -> UserFavorite:
        """:raises UserFavoriteNotFoundException:"""
        user_favorite: UserFavorite | None = UserFavorite.objects.filter(
            user_id=user_id.value, project_id=project_id.value
        ).first()
        if user_favorite is None:
            raise UserFavoriteNotFoundException(
                f"UserFavorite with (user_id={user_id.value}, project_id={project_id.value}) not found."
            )
        return user_favorite


class DjUserFavoriteWriteRepository(UserFavoriteWriteRepository):
    def create(self, data: UserFavoriteCreatePayload) -> UserFavorite:
        user_favorite = UserFavorite.objects.create(user_id=data.user_id.value, project_id=data.project_id.value)
        return user_favorite

    def update(self, data: UserFavoriteUpdatePayload) -> UserFavorite:
        raise NotImplementedError("Method update() not supported for UserFavorite.")

    def delete(self, id_: Id) -> None:
        """:raises UserFavoriteNotFoundException:"""
        try:
            user_favorite: UserFavorite = UserFavorite.objects.get(id=id_.value)
            user_favorite.delete()
        except UserFavorite.DoesNotExist:
            raise UserFavoriteNotFoundException(f"UserFavorite with id = {id_.value} not found.")

    def delete_by_association_ids(self, user_id: Id, project_id: Id) -> None:
        """:raises UserFavoriteNotFoundException:"""
        try:
            user_favorite: UserFavorite = UserFavorite.objects.get(user_id=user_id.value, project_id=project_id.value)
            user_favorite.delete()
        except UserFavorite.DoesNotExist:
            raise UserFavoriteNotFoundException(f"UserFavorite with ({user_id.value}, {project_id.value}) not found.")
