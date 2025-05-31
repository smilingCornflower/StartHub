from domain.exceptions.project_social_link import ProjectSocialLinkAlreadyExistsException
from domain.models.project import ProjectSocialLink
from domain.repositories.social_link import ProjectSocialLinkReadRepository, ProjectSocialLinkWriteRepository
from domain.value_objects.filter import ProjectSocialLinkFilter
from domain.value_objects.project_social_link import ProjectSocialLinkCreatePayload


class ProjectSocialLinkService:
    def __init__(
        self,
        read_repository: ProjectSocialLinkReadRepository,
        write_repository: ProjectSocialLinkWriteRepository,
    ):
        self._read_repository = read_repository
        self._write_repository = write_repository

    def create(self, payload: ProjectSocialLinkCreatePayload) -> ProjectSocialLink:
        """:raises ProjectSocialLinkAlreadyExistsException:"""

        filter_result: list[ProjectSocialLink] = self._read_repository.get_all(
            ProjectSocialLinkFilter(project_id=payload.project_id, social_link=payload.social_link)
        )
        if filter_result:
            raise ProjectSocialLinkAlreadyExistsException(
                f"social_link: {payload.social_link} already exists for the project with id = {payload.project_id.value}."
            )
        return self._write_repository.create(payload)
