from domain.models.geo.address import Address
from domain.repositories.geo.address import AddressReadRepository, AddressWriteRepository
from domain.value_objects.common import CursorPagination, Id, OffsetPagination
from domain.value_objects.filter import AddressFilter
from domain.value_objects.geo import AddressCreatePayload, AddressUpdatePayload
from infrastructure.repositories.pagination import apply_pagination


class DjAddressReadRepository(AddressReadRepository):
    def get_by_id(self, id_: Id) -> Address:
        raise NotImplementedError("The method get_by_id() is not implemented yet.")

    def get_all(
        self, filter_: AddressFilter, pagination: CursorPagination | OffsetPagination | None = None
    ) -> list[Address]:
        queryset = Address.objects.all().order_by("-id")

        if filter_.address_id:
            queryset = queryset.filter(id=filter_.address_id.value)
        if filter_.country_id:
            queryset = queryset.filter(country_id=filter_.country_id.value)
        if filter_.region_id:
            queryset = queryset.filter(region_id=filter_.region_id.value)
        if filter_.city_id:
            queryset = queryset.filter(city_id=filter_.city_id.value)
        if filter_.district:
            queryset = queryset.filter(district=filter_.district)
        if filter_.street:
            queryset = queryset.filter(street=filter_.street)
        if filter_.house_number:
            queryset = queryset.filter(house_number=filter_.house_number)
        if filter_.raw_address:
            queryset = queryset.filter(raw_address=filter_.raw_address)

        if pagination:
            return apply_pagination(queryset, pagination)
        return list(queryset.distinct())


class DjAddressWriteRepository(AddressWriteRepository):
    def create(self, data: AddressCreatePayload) -> Address:
        return Address.objects.create(
            country_id=data.country_id.value,
            region_id=data.region_id.value,
            city_id=data.city_id.value,
            district=data.district,
            street=data.street,
            house_number=data.house_number,
            postal_code=data.postal_code,
            raw_address=data.raw_address,
        )

    def update(self, data: AddressUpdatePayload) -> Address:
        raise NotImplementedError("The method update() is not implemented yet.")

    def delete_by_id(self, id_: Id) -> None:
        raise NotImplementedError("The method delete_by_id() is not implemented yet.")
