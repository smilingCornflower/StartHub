from domain.exceptions.project_management import ProjectImageNotFoundException
from domain.models.project_management.image import ProjectImage
from domain.repositories.project.image import ProjectImageReadRepository, ProjectImageWriteRepository
from domain.value_objects.common import Id, Pagination
from domain.value_objects.filter import ProjectImageFilter
from domain.value_objects.project.image import (
    ProjectImageCreatePayload,
    ProjectImageDeletePayload,
    ProjectImageUpdatePayload,
)


class DjProjectImageReadRepository(ProjectImageReadRepository):
    def get_by_id(self, id_: Id) -> ProjectImage:
        raise NotImplementedError("The method get_by_id() not implemented yet.")

    def get_all(self, filter_: ProjectImageFilter, pagination: Pagination | None = None) -> list[ProjectImage]:
        queryset = ProjectImage.objects.all()

        if filter_.project_id is not None:
            queryset = queryset.filter(project_id=filter_.project_id.value)

        if filter_.image_order is not None:
            queryset = queryset.filter(order=filter_.image_order)

        return list(queryset.distinct())


class DjProjectImageWriteRepository(ProjectImageWriteRepository):
    def create(self, data: ProjectImageCreatePayload) -> ProjectImage:
        return ProjectImage.objects.create(project_id=data.project_id.value, file_path=data.file_path, order=data.order)

    def update(self, data: ProjectImageUpdatePayload) -> ProjectImage:
        project_image: ProjectImage | None = ProjectImage.objects.filter(id=data.image_id.value).first()
        if project_image is None:
            raise ProjectImageNotFoundException(f"A project_image with id = {data.image_id.value} not found.")

        if data.order is not None:
            project_image.order = data.order.value
        project_image.save()
        return project_image

    def delete_by_id(self, id_: Id) -> None:
        raise NotImplementedError("The method delete() not implemented yet.")

    def delete(self, data: ProjectImageDeletePayload) -> None:
        ProjectImage.objects.filter(project_id=data.project_id.value, order=data.image_order).delete()
