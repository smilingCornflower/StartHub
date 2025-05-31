from datetime import date

from application.service_factories.company import CompanyServiceFactory
from application.services.company import CompanyAppService
from django.test import TestCase
from domain.exceptions.country import CountryNotFoundException
from domain.exceptions.user import UserNotFoundException
from domain.exceptions.validation import ValidationException
from domain.models.company import Company
from domain.models.country import Country
from domain.models.user import User
from pydantic import ValidationError


class CompanyAppServiceTests(TestCase):
    def setUp(self) -> None:
        self.valid_data = {
            "name": "Company Name",
            "country_code": "KZ",
            "business_number": "123456789012",
            "established_date": "2020-01-01",
            "description": "Description",
        }
        Country.objects.create(code="KZ")
        self.user = User.objects.create_user(
            email="test.email@example.com",
            username="test",
            password="TestPass1234",
        )
        self.service: CompanyAppService = CompanyServiceFactory().create_service()

    def test_valid_data(self) -> None:
        company: Company = self.service.create(request_data=self.valid_data, user_id=self.user.id)

        self.assertEqual(company.name, self.valid_data["name"])
        self.assertEqual(company.country.code, self.valid_data["country_code"])
        self.assertEqual(company.business_id, self.valid_data["business_number"])
        self.assertEqual(company.established_date, date.fromisoformat(self.valid_data["established_date"]))
        self.assertEqual(company.description, self.valid_data["description"])

    def test_missing_fields(self) -> None:
        for i in self.valid_data:
            data = self.valid_data.copy()
            data.pop(i)
            with self.assertRaises(KeyError):
                self.service.create(request_data=data, user_id=self.user.id)

    def test_invalid_country_code(self) -> None:
        data = self.valid_data.copy()
        data["country_code"] = "Kz"
        with self.assertRaises(ValidationError):
            self.service.create(request_data=data, user_id=self.user.id)

    def test_non_existing_country_code(self) -> None:
        data = self.valid_data.copy()
        data["country_code"] = "AT"
        with self.assertRaises(CountryNotFoundException):
            self.service.create(request_data=data, user_id=self.user.id)

    def test_invalid_business_number(self) -> None:
        data = self.valid_data.copy()
        data["business_number"] = "invalid-number"

        with self.assertRaises(ValidationException):
            self.service.create(request_data=data, user_id=self.user.id)

    def test_invalid_established_date(self) -> None:
        data = self.valid_data.copy()
        data["established_date"] = "2020.01.01"

        with self.assertRaises(ValidationError):
            self.service.create(request_data=data, user_id=self.user.id)

    def test_future_established_date(self) -> None:
        data = self.valid_data.copy()
        data["established_date"] = "2040-01-01"

        with self.assertRaises(ValidationException):
            self.service.create(request_data=data, user_id=self.user.id)

    def test_description_none(self) -> None:
        data = self.valid_data.copy()
        data["description"] = None  # type: ignore

    def test_another_type_fields(self) -> None:
        for i in self.valid_data:
            data = self.valid_data.copy()
            data[i] = 10  # type: ignore
            with self.subTest(data=data):
                with self.assertRaises(ValidationError):
                    self.service.create(request_data=data, user_id=self.user.id)

    def test_non_existing_user_id(self) -> None:
        with self.assertRaises(UserNotFoundException):
            self.service.create(request_data=self.valid_data, user_id=10)
