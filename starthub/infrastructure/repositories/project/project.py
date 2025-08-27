from domain.exceptions.project_management import ProjectNotFoundException
from domain.models.project_management.project import Project
from domain.repositories.project.project import ProjectReadRepository, ProjectWriteRepository
from domain.value_objects.common import CursorPagination, Id, OffsetPagination, Slug
from domain.value_objects.filter import ProjectFilter
from domain.value_objects.project.project import ProjectCreatePayload, ProjectUpdatePayload
from infrastructure.repositories.pagination import apply_pagination


class DjProjectReadRepository(ProjectReadRepository):
    def get_by_id(self, id_: Id) -> Project:
        """:raises ProjectNotFoundException:"""
        project: Project | None = Project.objects.filter(id=id_.value).first()

        if project is None:
            raise ProjectNotFoundException(f"Project with id = {id_.value} not found.")
        return project

    def get_all(
        self, filter_: ProjectFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[Project]:
        queryset = Project.objects.all().order_by("-id")

        if filter_.category_slug:
            queryset = queryset.filter(categories__slug=filter_.category_slug.value)
        if filter_.funding_model_slug:
            queryset = queryset.filter(funding_model__slug=filter_.funding_model_slug.value)
        if filter_.statuses:
            queryset = queryset.filter(status__in=[i.value for i in filter_.statuses])
        if filter_.stage:
            queryset = queryset.filter(stage=filter_.stage.value)
        if filter_.user_id:
            queryset = queryset.filter(creator_id=filter_.user_id.value)

        if filter_.exclude_statuses:
            queryset = queryset.exclude(status__in=[i.value for i in filter_.exclude_statuses])

        if pagination:
            return apply_pagination(queryset=queryset, pagination=pagination)
        return list(queryset.distinct())

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
            ltv=data.ltv.value if data.ltv is not None else None,
            arpu=data.arpu.value if data.arpu is not None else None,
            arppu=data.arppu.value if data.arppu is not None else None,
            cac=data.cac.value if data.cac is not None else None,
            nps=data.nps.value if data.nps is not None else None,
            roi=data.roi.value if data.roi is not None else None,
            aov=data.aov.value if data.aov is not None else None,
            churn_rate=data.churn_rate.value if data.churn_rate is not None else None,
            retention_rate=data.retention_rate.value if data.retention_rate is not None else None,
            conversion_rate=data.conversion_rate.value if data.conversion_rate is not None else None,
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

        if data.ltv is not None:
            project.ltv = data.ltv.value
        if data.arpu is not None:
            project.arpu = data.arpu.value
        if data.arppu is not None:
            project.arppu = data.arppu.value
        if data.cac is not None:
            project.cac = data.cac.value
        if data.nps is not None:
            project.nps = data.nps.value
        if data.roi is not None:
            project.roi = data.roi.value
        if data.aov is not None:
            project.aov = data.aov.value
        if data.churn_rate is not None:
            project.churn_rate = data.churn_rate.value
        if data.retention_rate is not None:
            project.retention_rate = data.retention_rate.value
        if data.conversion_rate is not None:
            project.conversion_rate = data.conversion_rate.value

        if data.status is not None:
            project.status = data.status.value

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
