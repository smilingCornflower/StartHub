from django.db.models import Q, QuerySet
from domain.exceptions.project_social_link import ProjectSocialLinkNotFoundException
from domain.models.project import ProjectSocialLink
from domain.repositories.social_link import ProjectSocialLinkReadRepository, ProjectSocialLinkWriteRepository
from domain.value_objects.common import Id
from domain.value_objects.filter import ProjectSocialLinkFilter
from domain.value_objects.project_social_link import ProjectSocialLinkCreatePayload, ProjectSocialLinkUpdatePayload


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
