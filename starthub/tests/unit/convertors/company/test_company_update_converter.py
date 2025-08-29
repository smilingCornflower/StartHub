from dataclasses import dataclass
from datetime import date
from unittest.mock import Mock

from django.test import SimpleTestCase
from domain.value_objects.common import Description, Id
from domain.value_objects.company import CompanyName, CompanyUpdateCommand, EstablishedDate, PatentNumber
from domain.value_objects.country import CountryCode
from domain.value_objects.geo import AddressCreateCommand, CityId, RegionId
from presentation.request_converters.company import request_to_company_update_command


@dataclass
class ValidCompanyUpdateData:
    company_id = 123
    name = "Test Company"
    description = "Test Company Description"
    established_date = "2020-01-15"
    patent_number = "PAT-2023-001"
    address = {
        "country_code": "KZ",
        "region_id": 1,
        "city_id": 5,
        "district": "Test District",
        "street": "Test Street",
        "house_number": "10A",
        "postal_code": "050000",
        "raw_address": "10A Test Street, Test District",
    }

    name_field = "name"
    description_field = "description"
    established_date_field = "established_date"
    patent_number_field = "patent_number"
    address_field = "address"

    def to_dict(self):
        return {
            self.name_field: self.name,
            self.description_field: self.description,
            self.established_date_field: self.established_date,
            self.patent_number_field: self.patent_number,
            self.address_field: self.address,
        }


class TestRequestToCompanyUpdateCommand(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidCompanyUpdateData()

    def test_valid_data_with_all_fields(self):
        request = Mock()
        request.data = self.valid_dataclass.to_dict()

        expected = CompanyUpdateCommand(
            company_id=Id(value=self.valid_dataclass.company_id),
            name=CompanyName(value=self.valid_dataclass.name),
            description=Description(value=self.valid_dataclass.description),
            established_date=EstablishedDate(value=date(2020, 1, 15)),
            address_create_command=AddressCreateCommand(
                country_code=CountryCode(value="KZ"),
                region_id=RegionId(value=1),
                city_id=CityId(value=5),
                district="Test District",
                street="Test Street",
                house_number="10A",
                postal_code="050000",
                raw_address="10A Test Street, Test District",
            ),
            patent_number=PatentNumber(value=self.valid_dataclass.patent_number),
        )

        result = request_to_company_update_command(request, self.valid_dataclass.company_id)
        self.assertEqual(expected, result)

    def test_empty_data(self):
        request = Mock()
        request.data = {}

        expected = CompanyUpdateCommand(
            company_id=Id(value=self.valid_dataclass.company_id),
            name=None,
            description=None,
            established_date=None,
            address_create_command=None,
            patent_number=None,
        )

        result = request_to_company_update_command(request, self.valid_dataclass.company_id)
        self.assertEqual(expected, result)
