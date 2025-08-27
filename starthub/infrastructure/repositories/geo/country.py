from domain.exceptions.geo.country import CountryNotFoundException
from domain.models.geo.country import Country
from domain.repositories.country import CountryReadRepository
from domain.value_objects.common import CursorPagination, Id, OffsetPagination
from domain.value_objects.country import CountryCode
from domain.value_objects.filter import CountryFilter


class DjCountryReadRepository(CountryReadRepository):
    def get_by_id(self, id_: Id) -> Country:
        """:raises CountryNotFoundException:"""
        country: Country | None = Country.objects.filter(id=id_.value).first()
        if country is None:
            raise CountryNotFoundException(f"Country with id = {id_.value} does not exist.")
        return country

    def get_all(
        self, filter_: CountryFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[Country]:
        queryset = Country.objects.all()

        if filter_.code:
            queryset = queryset.filter(code=filter_.code.value)

        return list(queryset)

    def get_by_code(self, code: CountryCode) -> Country:
        """:raises CountryNotFoundException:"""
        country: Country | None = Country.objects.filter(code=code.value).first()
        if country is None:
            raise CountryNotFoundException(f"Country with code '{code.value}' does not exist.")
        return country
