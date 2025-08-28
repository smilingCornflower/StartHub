from domain.exceptions.project_management import ProjectStageNotFoundException
from domain.models.project_management.project_stage import ProjectStage
from domain.repositories.project.stage import ProjectStageReadRepository, ProjectStageWriteRepository
from domain.value_objects.common import CursorPagination, OffsetPagination
from domain.value_objects.filter import ProjectStageFilter
from domain.value_objects.project.stage import ProjectStageCreatePayload, ProjectStageId, ProjectStageUpdatePayload


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


class DjProjectStageWriteRepository(ProjectStageWriteRepository):
    def create(self, data: ProjectStageCreatePayload) -> ProjectStage:
        raise NotImplementedError("The method create() is not implemented yet.")

    def update(self, data: ProjectStageUpdatePayload) -> ProjectStage:
        project_stage = ProjectStage.objects.filter(id=data.id_.value).first()
        if project_stage is None:
            raise ProjectStageNotFoundException(f"Project stage with = {data.id_.value} not found.")

        if data.description:
            project_stage.description = data.description.value

        project_stage.save()
        return project_stage

    def delete_by_id(self, id_: ProjectStageId) -> None:
        raise NotImplementedError("The method delete_by_id() is not implemented yet.")
