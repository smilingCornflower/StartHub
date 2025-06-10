from datetime import date, timedelta

import pydantic
from application.converters.request_converters.company import request_data_to_company_create_draft
from django.test import SimpleTestCase
from domain.exceptions.validation import ValidationException, DateIsNotIsoFormatException
from domain.value_objects.common import Id
from domain.value_objects.company import BusinessNumber
from domain.value_objects.country import CountryCode


class ConvertRequestDataToCompanyDraftTests(SimpleTestCase):
    def setUp(self) -> None:
        self.valid_payload = {
            "name": "ООО Технологии Будущего",
            "country_code": "KZ",
            "business_number": "123456789012",
            "established_date": "2020-01-01",
            "description": "Инновационные технологии",
        }
        self.user_id = 1

    def test_converts_valid_data_correctly(self) -> None:
        result = request_data_to_company_create_draft(self.valid_payload, user_id=self.user_id)

        self.assertEqual(result.name, "ООО Технологии Будущего")
        self.assertEqual(result.representative_id, Id(value=1))
        self.assertEqual(result.country_code, CountryCode(value="KZ"))
        self.assertEqual(result.business_id, BusinessNumber(country_code=CountryCode(value="KZ"), value="123456789012"))
        self.assertEqual(result.established_date, date(2020, 1, 1))
        self.assertEqual(result.description, "Инновационные технологии")

    def test_requires_all_mandatory_fields(self) -> None:
        mandatory_fields = ["name", "country_code", "business_number", "established_date"]

        for field in mandatory_fields:
            with self.subTest(field=field):
                invalid_data = self.valid_payload.copy()
                del invalid_data[field]

                with self.assertRaises(KeyError):
                    request_data_to_company_create_draft(invalid_data, self.user_id)

    def test_empty_description_handling(self) -> None:
        test_data = self.valid_payload.copy()
        test_data["description"] = ""

        result = request_data_to_company_create_draft(test_data, self.user_id)
        self.assertEqual(result.description, "")

    def test_none_description(self) -> None:
        self.valid_payload["description"] = None  # type: ignore

        with self.assertRaises(pydantic.ValidationError):
            request_data_to_company_create_draft(self.valid_payload, self.user_id)

    def test_rejects_invalid_date_formats(self) -> None:
        invalid_formats = [
            "01.01.2020",
            "01/01/2020",
            "01-Jan-2020",
            "2020-1-1",
            "20-01-01",
            "2020-13-01",
            "2020-01-32",
        ]

        for date_str in invalid_formats:
            with self.subTest(date_format=date_str):
                test_data = self.valid_payload.copy()
                test_data["established_date"] = date_str
                with self.assertRaises(ValueError):
                    request_data_to_company_create_draft(test_data, self.user_id)

    def test_accepts_valid_iso_formats(self) -> None:
        valid_formats = [
            "2020-01-01",
            "20200101",
        ]

        for date_str in valid_formats:
            test_data = self.valid_payload.copy()
            test_data["established_date"] = date_str
            result = request_data_to_company_create_draft(test_data, self.user_id)
            self.assertIsInstance(result.established_date, date)

    def test_rejects_future_dates(self) -> None:
        future_dates = [
            (date.today() + timedelta(days=1)).isoformat(),
            (date.today().replace(year=date.today().year + 1)).isoformat(),
            "2030-01-01",
        ]

        for future_date in future_dates:
            test_data = self.valid_payload.copy()
            test_data["established_date"] = future_date
            with self.assertRaises(ValidationException):
                request_data_to_company_create_draft(test_data, self.user_id)
