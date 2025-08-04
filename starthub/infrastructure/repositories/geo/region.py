from domain.exceptions.geo.region import RegionNotFoundException
from domain.models.geo.region import Region
from domain.repositories.geo.region import RegionReadRepository
from domain.value_objects.common import Id, Pagination
from domain.value_objects.filter import RegionFilter


class DjRegionReadRepository(RegionReadRepository):
    def get_by_id(self, id_: Id) -> Region:
        """:raises RegionNotFoundException:"""

        city: Region | None = Region.objects.filter(id=id_.value).first()
        if city is None:
            raise RegionNotFoundException(f"Region with id = {id_.value} does not exist.")
        return city

    def get_all(self, filter_: RegionFilter, pagination: Pagination | None = None) -> list[Region]:
        raise NotImplementedError("The method get_all() is not implemented yet.")
