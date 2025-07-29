from domain.ports.search import SearchParams
from domain.value_objects.project_management import ProjectName


class ProjectSearchParams(SearchParams):
    name: ProjectName | None = None
