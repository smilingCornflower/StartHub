from domain.exceptions.project_management import ProjectStageNotFoundException
from domain.models.project_management.project_stage import ProjectStage
from domain.repositories.project.stage import ProjectStageReadRepository
from domain.value_objects.common import CursorPagination, OffsetPagination
from domain.value_objects.filter import ProjectStageFilter
from domain.value_objects.project.stage import ProjectStageId


class DjProjectStageReadRepository(ProjectStageReadRepository):
    def get_by_id(self, id_: ProjectStageId) -> ProjectStage:
        """:raises ProjectStageNotFoundException:"""
        stage: ProjectStage | None = ProjectStage.objects.filter(id=id_.value).first()
        if stage is None:
            raise ProjectStageNotFoundException(f"ProjectStage with id = {id_.value} not found.")
        return stage

    def get_all(
        self, filter_: ProjectStageFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[ProjectStage]:
        raise NotImplementedError("The method is not implemented.")
