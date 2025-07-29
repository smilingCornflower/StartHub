from django.contrib.postgres.search import TrigramWordSimilarity
from domain.models.project import Project
from domain.ports.search import Search
from domain.value_objects.common import OffsetPagination
from domain.value_objects.search import ProjectSearchParams


class ProjectSearchService(Search[ProjectSearchParams, Project]):
    def search(self, search_params: ProjectSearchParams, pagination: OffsetPagination) -> list[Project]:
        qs = Project.objects.all()
        if search_params.name is not None:
            qs = (
                qs.annotate(similarity=TrigramWordSimilarity(search_params.name.value, "name"))
                .filter(similarity__gt=0.3)
                .order_by("similarity")
            )
        qs = qs[pagination.offset : pagination.offset + pagination.limit]
        return list(qs)
