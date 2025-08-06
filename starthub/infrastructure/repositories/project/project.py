from domain.exceptions.project_management import ProjectNotFoundException
from domain.models.project_management.project import Project
from domain.repositories.project.project import ProjectReadRepository, ProjectWriteRepository
from domain.value_objects.common import Id, Pagination, Slug
from domain.value_objects.filter import ProjectFilter
from domain.value_objects.project.project import ProjectCreatePayload, ProjectUpdatePayload


class DjProjectReadRepository(ProjectReadRepository):
    def get_by_id(self, id_: Id) -> Project:
        """:raises ProjectNotFoundException:"""
        project: Project | None = Project.objects.filter(id=id_.value).first()

        if project is None:
            raise ProjectNotFoundException(f"Project with id = {id_.value} not found.")
        return project

    def get_all(self, filter_: ProjectFilter, pagination: Pagination | None = None) -> list[Project]:
        queryset = Project.objects.all().order_by("-id")

        if filter_.category_slug:
            queryset = queryset.filter(categories__slug=filter_.category_slug.value)
        if filter_.funding_model_slug:
            queryset = queryset.filter(funding_model__slug=filter_.funding_model_slug.value)
        if filter_.status:
            queryset = queryset.filter(status=filter_.status.value)
        if filter_.stage:
            queryset = queryset.filter(stage=filter_.stage.value)
        if filter_.user_id:
            queryset = queryset.filter(creator_id=filter_.user_id.value)

        if pagination and pagination.last_id is not None:
            queryset = queryset.filter(id__lt=pagination.last_id)

        if pagination and pagination.limit is not None:
            result = list(queryset.distinct()[: pagination.limit])
        else:
            result = list(queryset.distinct())
        return result

    def get_by_slug(self, slug: Slug) -> Project:
        """:raises ProjectNotFoundException:"""
        project: Project | None = Project.objects.filter(slug=slug.value).first()

        if project is None:
            raise ProjectNotFoundException
        return project


class DjProjectWriteRepository(ProjectWriteRepository):
    def create(self, data: ProjectCreatePayload) -> Project:
        project = Project.objects.create(
            name=data.name.value,
            goal_description=data.goal_description.value if data.goal_description else None,
            description=data.description.value,
            creator_id=data.user_id.value,
            funding_model_id=data.funding_model_id.value,
            stage=data.stage.value,
            status=data.status.value,
            goal_sum=data.goal_sum.value,
            deadline=data.deadline,
            plan=data.plan_path,
        )
        project.categories.set([i.value for i in data.category_ids])
        return project

    def update(self, data: ProjectUpdatePayload) -> Project:
        """:raises ProjectNotFoundException:"""
        project: Project | None = Project.objects.filter(id=data.id_.value).first()
        if project is None:
            raise ProjectNotFoundException(f"The project with id = {data.id_.value} is not found.")

        if data.name is not None:
            project.name = data.name.value
            project.slug = None
        if data.description is not None:
            project.description = data.description.value
        if data.goal_description is not None:
            project.goal_description = data.goal_description.value
        if data.goal_sum is not None:
            project.goal_sum = data.goal_sum.value
        if data.deadline is not None:
            project.deadline = data.deadline.value
        if data.stage is not None:
            project.stage = data.stage.value
        if data.category_ids is not None:
            project.categories.set([i.value for i in data.category_ids])
        if data.funding_model_id is not None:
            project.funding_model_id = data.funding_model_id.value
        if data.plan_path is not None:
            project.plan = data.plan_path

        project.save()
        return project

    def delete_by_id(self, id_: Id) -> None:
        """:raises ProjectNotFoundException:"""
        try:
            project: Project = Project.objects.get(id=id_.value)
        except Project.DoesNotExist:
            raise ProjectNotFoundException(f"The project with id = {id_.value} is not found.")
        project.delete()

    def delete(self, project: Project) -> None:
        project.delete()

    @staticmethod
    def deactivate(id_: Id) -> None:
        """:raises ProjectNotFoundException:"""
        try:
            project: Project = Project.objects.get(id=id_.value)
            project.is_active = False
            project.save()
        except Project.DoesNotExist:
            raise ProjectNotFoundException(f"The project with id = {id_.value} is not found.")
