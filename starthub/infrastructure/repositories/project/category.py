from domain.exceptions.project_management import ProjectCategoryNotFoundException
from domain.models.project_management.category import ProjectCategory
from domain.repositories.project.category import ProjectCategoryReadRepository
from domain.value_objects.common import Id, Pagination
from domain.value_objects.filter import ProjectCategoryFilter
from infrastructure.repositories.pagination import apply_pagination


class DjProjectCategoryReadRepository(ProjectCategoryReadRepository):
    def get_by_id(self, id_: Id) -> ProjectCategory:
        """:raises ProjectCategoryNotFoundException:"""
        project_category: ProjectCategory | None = ProjectCategory.objects.filter(id=id_.value).first()

        if project_category is None:
            raise ProjectCategoryNotFoundException(f"Project category with id = {id_.value} does not exist.")

        return project_category

    def get_all(self, filter_: ProjectCategoryFilter, pagination: Pagination | None = None) -> list[ProjectCategory]:
        queryset = ProjectCategory.objects.all()

        if filter_.project_id is not None:
            queryset = queryset.filter(projects__id=filter_.project_id.value)
        if filter_.category_ids is not None:
            queryset = queryset.filter(id__in=[i.value for i in filter_.category_ids])

        if pagination:
            return apply_pagination(queryset, pagination=pagination)

        return list(queryset.distinct())
