from domain.models.project import Project
from domain.ports.search import Search
from domain.value_objects.common import OffsetPagination
from domain.value_objects.search import ProjectSearchParams


class ProjectSearchService(Search[ProjectSearchParams, Project]):
    def search(self, search_params: ProjectSearchParams, pagination: OffsetPagination) -> list[Project]:
        qs = Project.objects.all()
        if search_params.name is not None:
            qs = qs.filter(name__trigram_word_similar=search_params.name.value)
        qs = qs.distinct()
        qs = qs[pagination.offset : pagination.limit + pagination.limit]
        return list(qs)
