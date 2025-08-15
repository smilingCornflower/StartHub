from domain.exceptions.project_management import ProjectFileNotFoundException
from domain.models.project_management.project_file import ProjectFile
from domain.repositories.project.project_file import ProjectFileReadRepository, ProjectFileWriteRepository
from domain.value_objects.common import Pagination
from domain.value_objects.filter import ProjectFileFilter
from domain.value_objects.project.project_file import ProjectFileCreatePayload, ProjectFileId, ProjectFileUpdatePayload
from infrastructure.repositories.pagination import apply_pagination


class DjProjectFileReadRepository(ProjectFileReadRepository):
    def get_by_id(self, id_: ProjectFileId) -> ProjectFile:
        """:raises ProjectFileNotFoundException:"""
        project_file: ProjectFile | None = ProjectFile.objects.filter(id=id_.value).first()
        if project_file is None:
            raise ProjectFileNotFoundException(f"Project file with id = {id_.value} not found.")
        return project_file

    def get_all(self, filter_: ProjectFileFilter, pagination: Pagination | None = None) -> list[ProjectFile]:
        queryset = ProjectFile.objects.all()

        if filter_.project_id is not None:
            queryset = queryset.filter(project_id=filter_.project_id.value)

        if pagination:
            return apply_pagination(queryset=queryset, pagination=pagination)

        return list(queryset)


class DjProjectFileWriteRepository(ProjectFileWriteRepository):
    def create(self, data: ProjectFileCreatePayload) -> ProjectFile:
        return ProjectFile.objects.create(
            project_id=data.project_id.value,
            file_path=data.file_path,
            name=data.name.value if data.name is not None else None,
        )

    def update(self, data: ProjectFileUpdatePayload) -> ProjectFile:
        raise NotImplementedError("The method update() is not implemented yet.")

    def delete_by_id(self, id_: ProjectFileId) -> None:
        raise NotImplementedError("The method delete_by_id() is not implemented yet.")

    def delete(self, project_file: ProjectFile) -> None:
        project_file.delete()
