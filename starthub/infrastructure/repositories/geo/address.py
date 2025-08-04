from domain.models.geo.address import Address
from domain.repositories.geo.address import AddressReadRepository, AddressWriteRepository
from domain.value_objects.common import Id, Pagination
from domain.value_objects.filter import AddressFilter
from domain.value_objects.geo import AddressCreatePayload, AddressUpdatePayload


class DjAddressReadRepository(AddressReadRepository):
    def get_by_id(self, id_: Id) -> Address:
        raise NotImplementedError("The method get_by_id() is not implemented yet.")

    def get_all(self, filter_: AddressFilter, pagination: Pagination | None = None) -> list[Address]:
        raise NotImplementedError("The method get_all() is not implemented yet.")


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
