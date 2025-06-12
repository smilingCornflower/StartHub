from django.db.models import Q, QuerySet
from domain.exceptions.project_management import (
    FundingModelNotFoundException,
    ProjectCategoryNotFoundException,
    ProjectNotFoundException,
    ProjectPhoneAlreadyExistsException,
    ProjectPhoneNotFoundException,
    ProjectSocialLinkNotFoundException,
    TeamMemberNotFoundException,
)
from domain.models.funding_model import FundingModel
from domain.models.project import Project, ProjectPhone, ProjectSocialLink, TeamMember
from domain.models.project_category import ProjectCategory
from domain.repositories.project_management import (
    FundingModelReadRepository,
    ProjectCategoryReadRepository,
    ProjectPhoneReadRepository,
    ProjectPhoneWriteRepository,
    ProjectReadRepository,
    ProjectSocialLinkReadRepository,
    ProjectSocialLinkWriteRepository,
    ProjectWriteRepository,
    TeamMemberReadRepository,
    TeamMemberWriteRepository,
)
from domain.value_objects.common import Id, Slug
from domain.value_objects.filter import (
    FundingModelFilter,
    ProjectCategoryFilter,
    ProjectFilter,
    ProjectPhoneFilter,
    ProjectSocialLinkFilter,
    TeamMemberFilter,
)
from domain.value_objects.project_management import (
    ProjectCreatePayload,
    ProjectPhoneCreatePayload,
    ProjectPhoneUpdatePayload,
    ProjectSocialLinkCreatePayload,
    ProjectSocialLinkUpdatePayload,
    ProjectUpdatePayload,
    TeamMemberCreatePayload,
    TeamMemberUpdatePayload,
)
from loguru import logger


class DjProjectReadRepository(ProjectReadRepository):
    def get_by_id(self, id_: Id) -> Project:
        """:raises ProjectNotFoundException:"""
        project: Project | None = Project.objects.filter(id=id_.value).first()

        if project is None:
            raise ProjectNotFoundException(f"Project with id = {id_.value} not found.")
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


class DjProjectWriteRepository(ProjectWriteRepository):
    def create(self, data: ProjectCreatePayload) -> Project:
        project = Project.objects.create(
            name=data.name,
            description=data.description,
            category_id=data.category_id.value,
            creator_id=data.creator_id.value,
            company_id=data.company_id.value,
            funding_model_id=data.funding_model_id.value,
            stage=data.stage.value,
            goal_sum=data.goal_sum,
            deadline=data.deadline,
        )
        return project

    def update(self, data: ProjectUpdatePayload) -> Project:
        """:raises ProjectNotFoundException:"""
        project: Project | None = Project.objects.filter(id=data.id_.value).first()
        if project is None:
            raise ProjectNotFoundException(f"The project with id = {data.id_.value} is not found.")

        if data.name is not None:
            project.name = data.name
            project.slug = None
        if data.description is not None:
            project.description = data.description
        if data.goal_sum is not None:
            project.goal_sum = data.goal_sum
        if data.deadline is not None:
            project.deadline = data.deadline
        if data.stage is not None:
            project.stage = data.stage.value
        if data.category_id is not None:
            project.category_id = data.category_id.value
        if data.funding_model_id is not None:
            project.funding_model_id = data.funding_model_id.value
        if data.plan is not None:
            project.plan = data.plan

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
        """:raises ProjectNotFoundException:"""
        try:
            project: Project = Project.objects.get(id=id_.value)
            project.is_active = False
            project.save()
        except Project.DoesNotExist:
            raise ProjectNotFoundException(f"The project with id = {id_.value} is not found.")


class DjProjectCategoryReadRepository(ProjectCategoryReadRepository):
    def get_by_id(self, id_: Id) -> ProjectCategory:
        """:raises ProjectCategoryNotFoundException:"""
        project_category: ProjectCategory | None = ProjectCategory.objects.filter(id=id_.value).first()

        if project_category is None:
            raise ProjectCategoryNotFoundException(f"Project category with id = {id_.value} does not exist.")

        return project_category

    def get_all(self, filter_: ProjectCategoryFilter) -> list[ProjectCategory]:
        return list(ProjectCategory.objects.all())


class DjProjectPhoneReadRepository(ProjectPhoneReadRepository):
    def get_by_id(self, id_: Id) -> ProjectPhone:
        """:raises ProjectPhoneNotFoundException:"""
        project_phone: ProjectPhone | None = ProjectPhone.objects.filter(id=id_.value).first()
        if project_phone is None:
            raise ProjectPhoneNotFoundException(f"Project phone with id = {id_.value} not found.")
        return project_phone

    def get_all(self, filter_: ProjectPhoneFilter) -> list[ProjectPhone]:
        queryset: QuerySet[ProjectPhone] = ProjectPhone.objects.all()
        if filter_.project_id:
            queryset = queryset.filter(project_id=filter_.project_id.value)
        if filter_.number:
            queryset = queryset.filter(number=filter_.number.value)
        return list(queryset.distinct())


class DjProjectPhoneWriteRepository(ProjectPhoneWriteRepository):
    def create(self, data: ProjectPhoneCreatePayload) -> ProjectPhone:
        """:raises ProjectPhoneAlreadyExistsException:"""
        if ProjectPhone.objects.filter(Q(project_id=data.project_id.value) & Q(number=data.number.value)).exists():
            raise ProjectPhoneAlreadyExistsException(
                f"For the project with id = {data.project_id.value} this number already exists."
            )

        return ProjectPhone.objects.create(project_id=data.project_id.value, number=data.number.value)

    def update(self, data: ProjectPhoneUpdatePayload) -> ProjectPhone:
        """:raises ProjectPhoneNotFoundException:"""
        project_phone: ProjectPhone | None = ProjectPhone.objects.filter(id=data.phone_id.value).first()
        if project_phone is None:
            raise ProjectPhoneNotFoundException(f"Project phone with id = {data.phone_id} not found.")
        project_phone.number = data.number.value
        project_phone.save()
        return project_phone

    def delete(self, id_: Id) -> None:
        """:raises ProjectPhoneNotFoundException:"""
        try:
            ProjectPhone.objects.get(id=id_.value).delete()
        except ProjectPhone.DoesNotExist:
            raise ProjectPhoneNotFoundException(f"Project phone with id = {id_.value} not found.")


class DjProjectSocialLinkReadRepository(ProjectSocialLinkReadRepository):
    def get_by_id(self, id_: Id) -> ProjectSocialLink:
        social_link: ProjectSocialLink | None = ProjectSocialLink.objects.filter(id=id_.value).first()
        if social_link is None:
            raise ProjectSocialLinkNotFoundException(f"project social link with id = {id_.value} not found.")
        return social_link

    def get_all(self, filter_: ProjectSocialLinkFilter) -> list[ProjectSocialLink]:
        queryset: QuerySet[ProjectSocialLink] = ProjectSocialLink.objects.all()
        if filter_.project_id:
            queryset = queryset.filter(id=filter_.project_id.value)
        if filter_.social_link:
            queryset = queryset.filter(Q(platform=filter_.social_link.platform) & Q(url=filter_.social_link.link))
        return list(queryset.distinct())


class DjProjectSocialLinkWriteRepository(ProjectSocialLinkWriteRepository):
    def create(self, data: ProjectSocialLinkCreatePayload) -> ProjectSocialLink:
        return ProjectSocialLink.objects.create(
            project_id=data.project_id.value,
            platform=data.social_link.platform,
            url=data.social_link.link,
        )

    def update(self, data: ProjectSocialLinkUpdatePayload) -> ProjectSocialLink:
        raise NotImplementedError("Method update() is not implemented yet.")

    def delete(self, id_: Id) -> None:
        raise NotImplementedError("Method delete() is not implemented yet.")


class DjTeamMemberReadRepository(TeamMemberReadRepository):
    def get_by_id(self, id_: Id) -> TeamMember:
        team_member: TeamMember | None = TeamMember.objects.filter(id=id_.value).first()
        if team_member is None:
            raise TeamMemberNotFoundException(f"Team member with id = {id_.value} does not exist.")
        return team_member

    def get_all(self, filter_: TeamMemberFilter) -> list[TeamMember]:
        return list(TeamMember.objects.all())


class DjTeamMemberWriteRepository(TeamMemberWriteRepository):
    def create(self, data: TeamMemberCreatePayload) -> TeamMember:
        return TeamMember.objects.create(
            project_id=data.project_id.value,
            name=data.first_name.value,
            surname=data.last_name.value,
            description=data.description,
        )

    def update(self, data: TeamMemberUpdatePayload) -> TeamMember:
        """:raises NotImplementedError:"""
        raise NotImplementedError("Method update is not implemented yet.")

    def delete(self, id_: Id) -> None:
        """:raises NotImplementedError:"""
        raise NotImplementedError("Method delete is not implemented yet.")


class DjFundingModelReadRepository(FundingModelReadRepository):
    def get_by_id(self, id_: Id) -> FundingModel:
        """:raises FundingModelNotFoundException:"""
        funding_model: FundingModel | None = FundingModel.objects.filter(id=id_.value).first()
        if funding_model is None:
            raise FundingModelNotFoundException(f"Funding models with id = {id_.value} does not exist.")
        return funding_model

    def get_all(self, filter_: FundingModelFilter) -> list[FundingModel]:
        return list(FundingModel.objects.all())
