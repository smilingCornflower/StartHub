from domain.exceptions.project_phone import ProjectPhoneAlreadyExistsException
from domain.models.project import ProjectPhone
from domain.repositories.project_phone import ProjectPhoneReadRepository, ProjectPhoneWriteRepository
from domain.value_objects.filter import ProjectPhoneFilter
from domain.value_objects.project_phone import ProjectPhoneCreatePayload


class ProjectPhoneService:
    def __init__(
        self,
        project_phone_read_repository: ProjectPhoneReadRepository,
        project_phone_write_repository: ProjectPhoneWriteRepository,
    ):
        self._read_repository = project_phone_read_repository
        self._write_repository = project_phone_write_repository

    def create(self, payload: ProjectPhoneCreatePayload) -> ProjectPhone:
        """:raises ProjectPhoneAlreadyExistsException:"""

        filter_result: list[ProjectPhone] = self._read_repository.get_all(
            ProjectPhoneFilter(project_id=payload.project_id, number=payload.number)
        )
        if filter_result:
            raise ProjectPhoneAlreadyExistsException(
                f"This phone number is already assigned to the project with id = {payload.project_id}"
            )
        return self._write_repository.create(payload)
