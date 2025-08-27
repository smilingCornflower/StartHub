from domain.exceptions.geo.region import RegionNotFoundException
from domain.models.geo.region import Region
from domain.repositories.geo.region import RegionReadRepository
from domain.value_objects.common import CursorPagination, Id, OffsetPagination
from domain.value_objects.filter import RegionFilter
from infrastructure.repositories.pagination import apply_pagination


class DjRegionReadRepository(RegionReadRepository):
    def get_by_id(self, id_: Id) -> Region:
        """:raises RegionNotFoundException:"""

        city: Region | None = Region.objects.filter(id=id_.value).first()
        if city is None:
            raise RegionNotFoundException(f"Region with id = {id_.value} does not exist.")
        return city

    def get_all(
        self, filter_: RegionFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[Region]:
        queryset = Region.objects.all()

        if pagination:
            return apply_pagination(queryset, pagination=pagination)

        return list(queryset)
