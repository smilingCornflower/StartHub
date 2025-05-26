from domain.exceptions.project import ProjectNotFoundException
from domain.models.project import Project
from domain.repositories.project import ProjectReadRepository, ProjectWriteRepository
from domain.value_objects.common import Id, Slug
from domain.value_objects.filter import ProjectFilter
from domain.value_objects.project import ProjectCreatePayload, ProjectUpdatePayload
from loguru import logger


class DjReadRepository(ProjectReadRepository):
    def get_by_id(self, id_: Id) -> Project:
        """:raises ProjectNotFoundException:"""
        project: Project | None = Project.objects.filter(id=id_.value).first()

        if project is None:
            raise ProjectNotFoundException
        return project

    def get_all(self, filter_: ProjectFilter) -> list[Project]:
        queryset = Project.objects.all()

        if filter_.category_slug:
            queryset = queryset.filter(category__slug=filter_.category_slug.value)

        logger.debug(f'SQL statement = {str(queryset.query).replace('"', '')}')
        return list(queryset.distinct())

    def get_by_slug(self, slug: Slug) -> Project:
        """:raises ProjectNotFoundException:"""
        project: Project | None = Project.objects.filter(slug=slug.value).first()

        if project is None:
            raise ProjectNotFoundException
        return project


class DjWriteRepository(ProjectWriteRepository):
    def create(self, data: ProjectCreatePayload) -> Project:
        project = Project.objects.create(
            name=data.name,
            description=data.description,
            category_id=data.category_id.value,
            creator_id=data.creator_id.value,
            funding_model_id=data.funding_model_id.value,
            goal_sum=data.goal_sum,
            deadline=data.deadline,
        )
        project.team.set([id_.value for id_ in data.team_ids])
        return project

    def update(self, data: ProjectUpdatePayload) -> Project:
        """:raises ProjectNotFoundException:"""
        project: Project | None = Project.objects.filter(id=data.id_.value).first()
        if project is None:
            raise ProjectNotFoundException(f"The project with id = {data.id_.value} is not found.")

        if data.name is not None:
            project.name = data.name
        if data.description is not None:
            project.description = data.description
        if data.goal_sum is not None:
            project.goal_sum = data.goal_sum
        if data.deadline is not None:
            project.deadline = data.deadline
        if data.category_id is not None:
            project.category_id = data.category_id.value
        if data.add_team_ids:
            project.team.add(*[i.value for i in data.add_team_ids])
        if data.remove_team_ids:
            project.team.remove(*[i.value for i in data.remove_team_ids])

        project.save()
        return project

    def delete(self, id_: Id) -> None:
        """:raises ProjectNotFoundException:"""
        try:
            project: Project = Project.objects.get(id=id_.value)
        except Project.DoesNotExist:
            raise ProjectNotFoundException(f"The project with id = {id_.value} is not found.")
        project.delete()

    @staticmethod
    def deactivate(id_: Id) -> None:
        try:
            project: Project = Project.objects.get(id=id_.value)
            project.is_active = False
            project.save()
        except Project.DoesNotExist:
            raise ProjectNotFoundException(f"The project with id = {id_.value} is not found.")
