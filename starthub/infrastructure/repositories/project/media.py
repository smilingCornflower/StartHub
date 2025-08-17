from domain.exceptions.project_management import ProjectMediaNotFoundException
from domain.models.project_management.media import ProjectMedia
from domain.repositories.project.media import ProjectMediaReadRepository, ProjectMediaWriteRepository
from domain.value_objects.common import Pagination
from domain.value_objects.filter import ProjectMediaFilter
from domain.value_objects.project.media import ProjectMediaCreatePayload, ProjectMediaId, ProjectMediaUpdatePayload
from infrastructure.repositories.pagination import apply_pagination


class DjProjectMediaReadRepository(ProjectMediaReadRepository):
    def get_by_id(self, id_: ProjectMediaId) -> ProjectMedia:
        """:raises ProjectMediaNotFoundException:"""
        project_media: ProjectMedia | None = ProjectMedia.objects.filter(id=id_.value).first()

        if project_media is None:
            raise ProjectMediaNotFoundException(f"Project media with id = {id_.value} not found.")

        return project_media

    def get_all(self, filter_: ProjectMediaFilter, pagination: Pagination | None = None) -> list[ProjectMedia]:
        queryset = ProjectMedia.objects.all()

        if filter_.project_id is not None:
            queryset = queryset.filter(project_id=filter_.project_id.value)

        if pagination:
            return apply_pagination(queryset=queryset, pagination=pagination)

        return list(queryset)


class DjProjectMediaWriteRepository(ProjectMediaWriteRepository):
    def create(self, data: ProjectMediaCreatePayload) -> ProjectMedia:
        return ProjectMedia.objects.create(
            project_id=data.project_id.value,
            file_path=data.file_path,
            order=data.order,
        )

    def update(self, data: ProjectMediaUpdatePayload) -> ProjectMedia:
        media: ProjectMedia | None = ProjectMedia.objects.filter(id=data.media_id.value).first()
        if media is None:
            raise ProjectMediaNotFoundException(f"Media with id = {data.media_id.value} does not found.")

        if data.order is not None:
            media.order = data.order.value

        media.save()
        return media

    def delete_by_id(self, id_: ProjectMediaId) -> None:
        raise NotImplementedError("The method delete_by_id() is not implemented yet.")

    def delete(self, project_media: ProjectMedia) -> None:
        project_media.delete()
