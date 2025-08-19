from domain.exceptions.project_management import ProjectUsefulLinkNotFoundException
from domain.models.project_management.useful_link import ProjectUsefulLink
from domain.repositories.project.useful_link import ProjectUsefulLinkReadRepository, ProjectUsefulLinkWriteRepository
from domain.value_objects.common import Pagination
from domain.value_objects.filter import ProjectUsefulLinkFilter
from domain.value_objects.project.useful_link import UsefulLinkCreatePayload, UsefulLinkId, UsefulLinkUpdatePayload
from infrastructure.repositories.pagination import apply_pagination


class DjProjectUsefulLinkReadRepository(ProjectUsefulLinkReadRepository):
    def get_by_id(self, id_: UsefulLinkId) -> ProjectUsefulLink:
        """:raises ProjectUsefulLinkNotFoundException:"""

        useful_link: ProjectUsefulLink | None = ProjectUsefulLink.objects.filter(id=id_.value).first()
        if useful_link is None:
            raise ProjectUsefulLinkNotFoundException(f"Project useful link with id = {id_.value} not found.")

        return useful_link

    def get_all(
        self, filter_: ProjectUsefulLinkFilter, pagination: Pagination | None = None
    ) -> list[ProjectUsefulLink]:
        queryset = ProjectUsefulLink.objects.all()

        if filter_.project_id:
            queryset = queryset.filter(project_id=filter_.project_id.value)

        if filter_.useful_link:
            queryset = queryset.filter(url=filter_.useful_link)

        if pagination:
            return apply_pagination(queryset, pagination=pagination)

        return list(queryset)


class DjProjectUsefulLinkWriteRepository(ProjectUsefulLinkWriteRepository):
    def create(self, data: UsefulLinkCreatePayload) -> ProjectUsefulLink:
        return ProjectUsefulLink.objects.create(
            project_id=data.project_id.value,
            name=data.name.value,
            url=data.url,
        )

    def update(self, data: UsefulLinkUpdatePayload) -> ProjectUsefulLink:
        raise NotImplementedError("The method update() is not implemented yet.")

    def delete_by_id(self, id_: UsefulLinkId) -> None:
        raise NotImplementedError("The method delete_by_id() is not implemented yet.")

    def delete(self, link: ProjectUsefulLink) -> None:
        link.delete()
