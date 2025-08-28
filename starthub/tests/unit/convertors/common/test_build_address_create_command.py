from dataclasses import dataclass

from django.test import SimpleTestCase
from domain.exceptions.validation import MissingRequiredFieldException
from domain.value_objects.country import CountryCode
from domain.value_objects.geo import AddressCreateCommand, CityId, RegionId
from presentation.request_converters.common import build_address_create_command


@dataclass
class ValidAddressData:
    country_code = "KZ"
    region_id = 1
    city_id = 5
    district = "Almaly District"
    street = "Abay Avenue"
    house_number = "123A"
    postal_code = "050000"
    raw_address = "123A Abay Avenue, Almaly District, Almaty, Kazakhstan"

    country_code_field = "country_code"
    region_id_field = "region_id"
    city_id_field = "city_id"
    district_field = "district"
    street_field = "street"
    house_number_field = "house_number"
    postal_code_field = "postal_code"
    raw_address_field = "raw_address"

    def to_dict(self):
        return {
            self.country_code_field: self.country_code,
            self.region_id_field: self.region_id,
            self.city_id_field: self.city_id,
            self.district_field: self.district,
            self.street_field: self.street,
            self.house_number_field: self.house_number,
            self.postal_code_field: self.postal_code,
            self.raw_address_field: self.raw_address,
        }


class TestBuildAddressCreateCommand(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidAddressData()

    def test_valid_data_with_all_fields(self):
        address_data = self.valid_dataclass.to_dict()

        expected = AddressCreateCommand(
            country_code=CountryCode(value=self.valid_dataclass.country_code),
            region_id=RegionId(value=self.valid_dataclass.region_id),
            city_id=CityId(value=self.valid_dataclass.city_id),
            district=self.valid_dataclass.district,
            street=self.valid_dataclass.street,
            house_number=self.valid_dataclass.house_number,
            postal_code=self.valid_dataclass.postal_code,
            raw_address=self.valid_dataclass.raw_address,
        )

        result = build_address_create_command(address_data)
        self.assertEqual(expected, result)

    def test_valid_data_with_required_fields_only(self):
        address_data = {
            self.valid_dataclass.country_code_field: self.valid_dataclass.country_code,
            self.valid_dataclass.region_id_field: self.valid_dataclass.region_id,
            self.valid_dataclass.city_id_field: self.valid_dataclass.city_id,
        }

        expected = AddressCreateCommand(
            country_code=CountryCode(value=self.valid_dataclass.country_code),
            region_id=RegionId(value=self.valid_dataclass.region_id),
            city_id=CityId(value=self.valid_dataclass.city_id),
            district=None,
            street=None,
            house_number=None,
            postal_code=None,
            raw_address=None,
        )
        result = build_address_create_command(address_data)
        self.assertEqual(expected, result)

    def test_missing_country_code(self):
        address_data = self.valid_dataclass.to_dict()
        del address_data[self.valid_dataclass.country_code_field]

        with self.assertRaises(MissingRequiredFieldException):
            build_address_create_command(address_data)

    def test_missing_region_id(self):
        address_data = self.valid_dataclass.to_dict()
        del address_data[self.valid_dataclass.region_id_field]

        with self.assertRaises(MissingRequiredFieldException):
            build_address_create_command(address_data)

    def test_missing_city_id(self):
        address_data = self.valid_dataclass.to_dict()
        del address_data[self.valid_dataclass.city_id_field]

        with self.assertRaises(MissingRequiredFieldException):
            build_address_create_command(address_data)
