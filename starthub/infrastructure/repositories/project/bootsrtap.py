from domain.exceptions.project_management import ProjectBootstrapNotFoundException
from domain.models.project_management.bootstrap import ProjectBootstrap
from domain.repositories.project.bootstrap import ProjectBootstrapReadRepository, ProjectBootstrapWriteRepository
from domain.value_objects.common import Pagination
from domain.value_objects.filter import ProjectBootstrapFilter
from domain.value_objects.project.bootstrap import (
    ProjectBootstrapCreatePayload,
    ProjectBootstrapId,
    ProjectBootstrapUpdatePayload,
)
from infrastructure.repositories.pagination import apply_pagination


class DjProjectBootstrapReadRepository(ProjectBootstrapReadRepository):
    def get_by_id(self, id_: ProjectBootstrapId) -> ProjectBootstrap:
        """:raises ProjectBootsrtapNotFoundException:"""

        bootsrtap = ProjectBootstrap.objects.filter(id=id_.value).first()
        if bootsrtap is None:
            raise ProjectBootstrapNotFoundException(f"ProjectBootsrtap with id = {id_.value} not found.")
        return bootsrtap

    def get_all(self, filter_: ProjectBootstrapFilter, pagination: Pagination | None = None) -> list[ProjectBootstrap]:
        queryset = ProjectBootstrap.objects.all()

        if filter_.project_id is not None:
            queryset = queryset.filter(project_id=filter_.project_id.value)

        if pagination is not None:
            return apply_pagination(queryset=queryset, pagination=pagination)

        return list(queryset)


class DjProjectBootstrapWriteRepository(ProjectBootstrapWriteRepository):
    def create(self, data: ProjectBootstrapCreatePayload) -> ProjectBootstrap:
        return ProjectBootstrap.objects.create(project_id=data.project_id.value, description=data.description.value)

    def update(self, data: ProjectBootstrapUpdatePayload) -> ProjectBootstrap:
        bootsrtap = ProjectBootstrap.objects.filter(id=data.bootstrap_id.value).first()
        if bootsrtap is None:
            raise ProjectBootstrapNotFoundException(f"ProjectBootsrtap with id = {data.bootstrap_id.value} not found.")

        if data.description is not None:
            bootsrtap.description = data.description.value

        bootsrtap.save()
        return bootsrtap

    def delete_by_id(self, id_: ProjectBootstrapId) -> None:
        raise NotImplementedError("The method delete_by_id() is not implemented.")

    def delete(self, bootstrap: ProjectBootstrap) -> None:
        bootstrap.delete()
