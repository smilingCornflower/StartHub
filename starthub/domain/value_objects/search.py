from domain.ports.search import SearchParams
from domain.value_objects.project.common import ProjectName


class ProjectSearchParams(SearchParams):
    name: ProjectName | None = None
