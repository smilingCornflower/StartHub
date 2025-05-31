from domain.exceptions.project_category import ProjectCategoryNotFoundException
from domain.models.project_category import ProjectCategory
from domain.repositories.project_category import ProjectCategoryReadRepository
from domain.value_objects.common import Id
from domain.value_objects.filter import ProjectCategoryFilter

# TODO: Use class Id(int); instead of class Id: value: int


class DjProjectCategoryReadRepository(ProjectCategoryReadRepository):
    def get_by_id(self, id_: Id) -> ProjectCategory:
        """:raises ProjectCategoryNotFoundException:"""
        project_category: ProjectCategory | None = ProjectCategory.objects.filter(id=id_.value).first()

        if project_category is None:
            raise ProjectCategoryNotFoundException(f"Project category with id = {id_.value} does not exist.")

        return project_category

    def get_all(self, filter_: ProjectCategoryFilter) -> list[ProjectCategory]:
        return list(ProjectCategory.objects.all())
