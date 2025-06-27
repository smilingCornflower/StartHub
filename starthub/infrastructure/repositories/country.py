from domain.exceptions.country import CountryNotFoundException
from domain.models.country import Country
from domain.repositories.country import CountryReadRepository
from domain.value_objects.common import Id, Pagination
from domain.value_objects.filter import CountryFilter


class DjCountryReadRepository(CountryReadRepository):
    def get_by_id(self, id_: Id) -> Country:
        """:raises CountryNotFoundException:"""
        country: Country | None = Country.objects.filter(id=id_.value).first()
        if country is None:
            raise CountryNotFoundException(f"Country with id = {id_.value} does not exist.")
        return country

    def get_all(self, filter_: CountryFilter, pagination: Pagination | None = None) -> list[Country]:
        queryset = Country.objects.all()

        if filter_.code:
            queryset = queryset.filter(code=filter_.code.value)

        return list(queryset)
