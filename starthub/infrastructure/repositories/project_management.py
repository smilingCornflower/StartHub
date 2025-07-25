from django.db.models import Q, QuerySet
from domain.exceptions.project_management import (
    FundingModelNotFoundException,
    ProjectCategoryNotFoundException,
    ProjectImageNotFoundException,
    ProjectNotFoundException,
    ProjectPhoneAlreadyExistsException,
    ProjectPhoneNotFoundException,
    ProjectSocialLinkNotFoundException,
    TeamMemberNotFoundException,
)
from domain.models.funding_model import FundingModel
from domain.models.project import Project, ProjectImage, ProjectPhone, ProjectSocialLink, TeamMember
from domain.models.project_category import ProjectCategory
from domain.repositories.project_management import (
    FundingModelReadRepository,
    ProjectCategoryReadRepository,
    ProjectImageReadRepository,
    ProjectImageWriteRepository,
    ProjectPhoneReadRepository,
    ProjectPhoneWriteRepository,
    ProjectReadRepository,
    ProjectSocialLinkReadRepository,
    ProjectSocialLinkWriteRepository,
    ProjectWriteRepository,
    TeamMemberReadRepository,
    TeamMemberWriteRepository,
)
from domain.value_objects.common import Id, Pagination, Slug
from domain.value_objects.filter import (
    FundingModelFilter,
    ProjectCategoryFilter,
    ProjectFilter,
    ProjectImageFilter,
    ProjectPhoneFilter,
    ProjectSocialLinkFilter,
    TeamMemberFilter,
)
from domain.value_objects.project_management import (
    ProjectCreatePayload,
    ProjectImageCreatePayload,
    ProjectImageDeletePayload,
    ProjectImageUpdatePayload,
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

    def get_all(self, filter_: ProjectFilter, pagination: Pagination | None = None) -> list[Project]:
        queryset = Project.objects.all().order_by("-id")

        if filter_.category_slug:
            queryset = queryset.filter(category__slug=filter_.category_slug.value)
        if filter_.funding_model_slug:
            queryset = queryset.filter(funding_model__slug=filter_.funding_model_slug.value)
        if filter_.status:
            queryset = queryset.filter(status=filter_.status.value)
        if filter_.stage:
            queryset = queryset.filter(stage=filter_.stage.value)

        if pagination and pagination.last_id is not None:
            queryset = queryset.filter(id__lt=pagination.last_id)

        logger.debug(f'SQL statement = {str(queryset.query).replace('"', '')}')
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
            description=data.description.value,
            category_id=data.category_id.value,
            creator_id=data.creator_id.value,
            funding_model_id=data.funding_model_id.value,
            stage=data.stage.value,
            status=data.status.value,
            goal_sum=data.goal_sum.value,
            deadline=data.deadline,
        )
        return project

    def update(self, data: ProjectUpdatePayload) -> Project:
        """:raises ProjectNotFoundException:"""
        project: Project | None = Project.objects.filter(id=data.id_.value).first()
        if project is None:
            raise ProjectNotFoundException(f"The project with id = {data.id_.value} is not found.")

        if data.name is not None:
            project.name = data.name.value
            project.slug = None
        if data.goal_sum is not None:
            project.goal_sum = data.goal_sum.value
        if data.deadline is not None:
            project.deadline = data.deadline.value
        if data.stage is not None:
            project.stage = data.stage.value
        if data.category_id is not None:
            project.category_id = data.category_id.value
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

    def get_all(self, filter_: ProjectCategoryFilter, pagination: Pagination | None = None) -> list[ProjectCategory]:
        return list(ProjectCategory.objects.all())


class DjProjectPhoneReadRepository(ProjectPhoneReadRepository):
    def get_by_id(self, id_: Id) -> ProjectPhone:
        """:raises ProjectPhoneNotFoundException:"""
        project_phone: ProjectPhone | None = ProjectPhone.objects.filter(id=id_.value).first()
        if project_phone is None:
            raise ProjectPhoneNotFoundException(f"Project phone with id = {id_.value} not found.")
        return project_phone

    def get_all(self, filter_: ProjectPhoneFilter, pagination: Pagination | None = None) -> list[ProjectPhone]:
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

    def delete_by_id(self, id_: Id) -> None:
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

    def get_all(
        self, filter_: ProjectSocialLinkFilter, pagination: Pagination | None = None
    ) -> list[ProjectSocialLink]:
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

    def delete_by_id(self, id_: Id) -> None:
        raise NotImplementedError("Method delete() is not implemented yet.")


class DjTeamMemberReadRepository(TeamMemberReadRepository):
    def get_by_id(self, id_: Id) -> TeamMember:
        team_member: TeamMember | None = TeamMember.objects.filter(id=id_.value).first()
        if team_member is None:
            raise TeamMemberNotFoundException(f"Team member with id = {id_.value} does not exist.")
        return team_member

    def get_all(self, filter_: TeamMemberFilter, pagination: Pagination | None = None) -> list[TeamMember]:
        return list(TeamMember.objects.all())


class DjTeamMemberWriteRepository(TeamMemberWriteRepository):
    def create(self, data: TeamMemberCreatePayload) -> TeamMember:
        return TeamMember.objects.create(
            project_id=data.project_id.value,
            name=data.first_name.value,
            surname=data.last_name.value,
            description=data.description.value,
        )

    def update(self, data: TeamMemberUpdatePayload) -> TeamMember:
        """:raises NotImplementedError:"""
        raise NotImplementedError("Method update is not implemented yet.")

    def delete_by_id(self, id_: Id) -> None:
        """:raises NotImplementedError:"""
        raise NotImplementedError("Method delete is not implemented yet.")


class DjFundingModelReadRepository(FundingModelReadRepository):
    def get_by_id(self, id_: Id) -> FundingModel:
        """:raises FundingModelNotFoundException:"""
        funding_model: FundingModel | None = FundingModel.objects.filter(id=id_.value).first()
        if funding_model is None:
            raise FundingModelNotFoundException(f"Funding models with id = {id_.value} does not exist.")
        return funding_model

    def get_all(self, filter_: FundingModelFilter, pagination: Pagination | None = None) -> list[FundingModel]:
        return list(FundingModel.objects.all())


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

    def get_images_count_for_project(self, project_id: Id) -> int:
        return ProjectImage.objects.filter(project_id=project_id.value).count()


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
