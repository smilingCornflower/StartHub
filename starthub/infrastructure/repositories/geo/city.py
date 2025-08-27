from django.db.models import Q
from domain.enums.language import LangCodeEnum
from domain.exceptions.geo.city import CityNotFoundException
from domain.models.geo.city import City
from domain.repositories.geo.city import CityReadRepository
from domain.value_objects.common import CursorPagination, Id, OffsetPagination
from domain.value_objects.filter import CityFilter
from infrastructure.repositories.pagination import apply_pagination


class DjCityReadRepository(CityReadRepository):
    def get_by_id(self, id_: Id) -> City:
        """:raises CityNotFoundException:"""

        city: City | None = City.objects.filter(id=id_.value).first()
        if city is None:
            raise CityNotFoundException(f"City with id = {id_.value} does not exists.")
        return city

    def get_all(self, filter_: CityFilter, pagination: CursorPagination | OffsetPagination | None = None) -> list[City]:
        queryset = City.objects.all()

        if filter_.region_name is not None:
            q_objects = Q()
            for lang_code in LangCodeEnum:
                field = f"region__name_{lang_code}"
                q_objects |= Q(**{field: filter_.region_name.value})

            queryset = queryset.filter(q_objects)

        if pagination:
            return apply_pagination(queryset, pagination=pagination)

        return list(queryset.distinct())
