import json
import time

import pydantic
from config.settings import BASE_DIR
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from domain.exceptions.company import BusinessNumberAlreadyExistsException, CompanyNameIsTooLongException
from domain.exceptions.geo.country import CountryNotFoundException, InvalidCountryCodeException
from domain.exceptions.project_management import (
    FundingModelNotFoundException,
    InvalidProjectStageException,
    NegativeProjectGoalSumException,
    ProjectCategoryNotFoundException,
    ProjectNameIsTooLongException,
)
from domain.exceptions.validation import (
    DateInFutureException,
    DateIsNotIsoFormatException,
    DisallowedSocialLinkException,
    EmptyStringException,
    FirstNameIsTooLongException,
    InvalidSocialLinkException,
    LastNameIsTooLongException,
    MissingRequiredFieldException,
)
from domain.models import Country
from domain.models.funding_model import FundingModel
from domain.models.project_category import ProjectCategory
from domain.models.user import User
from loguru import logger
from presentation.response_factories.common import ProjectErrorResponseFactory
from rest_framework.response import Response
from rest_framework.test import APIClient


class TestProjectPost(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.project_url = reverse("projects")
        login_url = reverse("login")
        cls.client = APIClient()

        cls.user = User.objects.create_user(email="test@email.com", password="ValidPass1234")
        cls.funding_model = FundingModel.objects.create(name="Funding Model 1")
        cls.category_1 = ProjectCategory.objects.create(name="Category 1")
        cls.category_2 = ProjectCategory.objects.create(name="Category 2")
        cls.country = Country.objects.create(code="KZ")

        response = cls.client.post(
            login_url, data={"email": "test@email.com", "password": "ValidPass1234"}, content_type="application/json"
        )
        cls.access_token = response.json()["access_token"]
        cls.headers = {"Authorization": f"Bearer {cls.access_token}"}
        cls.pdf_path = BASE_DIR / "tests/files/The_C_Programming_Language.pdf"

    def setUp(self):
        with open(self.pdf_path, "rb") as f:
            self.valid_data = {
                "project": {
                    "name": "My Project",
                    "description": "Project description",
                    "category_ids": [self.category_1.id, self.category_2.id],
                    "funding_model_id": self.funding_model.id,
                    "stage": "idea",
                    "goal_sum": 100000,
                    "deadline": "2025-12-31",
                    "social_links": {"linkedin": "https://linkedin.com/in/example"},
                    "phone_number": "+77026882636",
                },
                "team_members": [{"first_name": "first_name", "last_name": "last_name", "description": "Developer"}],
                "company": {
                    "name": "Company Name",
                    "description": "Tech company",
                    "country_code": "KZ",
                    "business_id": "000000000000",
                    "established_date": "2020-01-01",
                },
                "company_founder": {"first_name": "John", "last_name": "Doe", "description": "CEO"},
                "project_plan": SimpleUploadedFile("dummy.pdf", f.read(), content_type="application/pdf"),
            }

    def _get_prepared_data(self):
        excluded = ["project_plan", "images"]
        result = {}
        for k, v in self.valid_data.items():
            if k not in excluded:
                result[k] = json.dumps(v)
            else:
                result[k] = v
        # refresh pdf file, to read it from the start
        with open(self.pdf_path, mode="rb") as f:
            result["project_plan"] = SimpleUploadedFile("dummy.pdf", f.read(), content_type="application/pdf")
        return result

    def _check_response(self, response, error_class, msg=""):
        app_code, http_code = ProjectErrorResponseFactory.error_codes[error_class]
        logger.debug(f"msg = {msg}\n\t {response.json()=}")
        self.assertEqual(response.json()["code"], app_code)
        self.assertEqual(response.status_code, http_code)

    def test_successful_crete(self):
        logger.warning("test_successful_crete")
        response: Response = self.client.post(self.project_url, data=self._get_prepared_data(), headers=self.headers)
        self.assertEqual(response.status_code, 201)

    def test_create_with_images(self):
        logger.warning("test_create_with_images")
        with open(BASE_DIR / "tests/images/miku.jpg", "rb") as f:
            miku_file = SimpleUploadedFile("miku.jpg", f.read(), content_type="image/jpeg")

        with open(BASE_DIR / "tests/images/Kawaii.png", "rb") as f:
            kawaii_file = SimpleUploadedFile("Kawaii.png", f.read(), content_type="image/png")
        self.valid_data["images"] = [miku_file, kawaii_file]
        response: Response = self.client.post(self.project_url, data=self._get_prepared_data(), headers=self.headers)
        self.assertEqual(response.status_code, 201)

    def test_missing_authorization_header(self):
        logger.warning("test_missing_authorization_header()")
        self._check_response(self.client.post(self.project_url, data=self.valid_data), MissingRequiredFieldException)

    def test_project_name_too_long(self):
        logger.warning("test_project_name_too_long()")
        self.valid_data["project"]["name"] = "a" * 256
        self._check_response(
            self.client.post(self.project_url, data=self._get_prepared_data(), headers=self.headers),
            ProjectNameIsTooLongException,
        )

    def test_business_id_exists(self):
        self.client.post(self.project_url, data=self._get_prepared_data(), headers=self.headers)
        time.sleep(10)
        self._check_response(
            self.client.post(self.project_url, data=self._get_prepared_data(), headers=self.headers),
            BusinessNumberAlreadyExistsException,
            msg="test_business_id_exists",
        )

    def test_category_not_found(self):
        self.valid_data["project"]["category_ids"] = [-1]
        self._check_response(
            self.client.post(self.project_url, data=self._get_prepared_data(), headers=self.headers),
            ProjectCategoryNotFoundException,
            msg="test_business_id_exists",
        )

    def test_funding_model_not_found(self):
        self.valid_data["project"]["funding_model_id"] = -1
        self._check_response(
            self.client.post(self.project_url, data=self._get_prepared_data(), headers=self.headers),
            FundingModelNotFoundException,
            msg="test_business_id_exists",
        )

    def test_invalid_stage(self):
        self.valid_data["project"]["stage"] = "invalid"
        self._check_response(
            self.client.post(self.project_url, data=self._get_prepared_data(), headers=self.headers),
            InvalidProjectStageException,
            msg="test_business_id_exists",
        )

    def test_negative_goal_sum(self):
        self.valid_data["project"]["goal_sum"] = -100
        self._check_response(
            self.client.post(self.project_url, data=self._get_prepared_data(), headers=self.headers),
            NegativeProjectGoalSumException,
            msg="test_business_id_exists",
        )

    def test_date_is_not_in_iso_format(self):
        self.valid_data["project"]["deadline"] = "2025.11.11"
        self._check_response(
            self.client.post(self.project_url, data=self._get_prepared_data(), headers=self.headers),
            DateIsNotIsoFormatException,
            msg="test_business_id_exists",
        )

    def test_disallowed_social_platforms(self):
        self.valid_data["project"]["social_links"] = {
            "linkedin": "https://linkedin.com/in/example",
            "chatgpt": "https://chatgpt.com/",
        }

        self._check_response(
            self.client.post(self.project_url, data=self._get_prepared_data(), headers=self.headers),
            DisallowedSocialLinkException,
            msg="test_business_id_exists",
        )

    def test_invalid_social_links(self):
        self.valid_data["project"]["social_links"] = {"linkedin": "https://lnkedin.com/in/example"}
        self._check_response(
            self.client.post(self.project_url, data=self._get_prepared_data(), headers=self.headers),
            InvalidSocialLinkException,
            msg="test_business_id_exists",
        )

    def test_invalid_data_type(self):
        self.valid_data["project"]["description"] = 1000
        self._check_response(
            self.client.post(self.project_url, data=self._get_prepared_data(), headers=self.headers),
            pydantic.ValidationError,
            msg="test_business_id_exists",
        )

    def test_missing_required_field(self):
        del self.valid_data["company"]
        self._check_response(
            self.client.post(self.project_url, data=self._get_prepared_data(), headers=self.headers),
            MissingRequiredFieldException,
            msg="test_business_id_exists",
        )

    def test_empty_string_not_allowed(self):
        self.valid_data["project"]["name"] = ""
        self._check_response(
            self.client.post(self.project_url, data=self._get_prepared_data(), headers=self.headers),
            EmptyStringException,
            msg="test_business_id_exists",
        )

    def test_first_name_too_long(self):
        self.valid_data["team_members"][0]["first_name"] = "a" * 256
        self._check_response(
            self.client.post(self.project_url, data=self._get_prepared_data(), headers=self.headers),
            FirstNameIsTooLongException,
            msg="test_business_id_exists",
        )

    def test_last_name_is_too_long(self):
        self.valid_data["team_members"][0]["last_name"] = "a" * 256
        self._check_response(
            self.client.post(self.project_url, data=self._get_prepared_data(), headers=self.headers),
            LastNameIsTooLongException,
            msg="test_business_id_exists",
        )

    def test_company_name_too_long(self):
        self.valid_data["company"]["name"] = "a" * 256
        self._check_response(
            self.client.post(self.project_url, data=self._get_prepared_data(), headers=self.headers),
            CompanyNameIsTooLongException,
            msg="test_business_id_exists",
        )

    def test_established_date_in_future(self):
        self.valid_data["company"]["established_date"] = "2030-01-01"
        self._check_response(
            self.client.post(self.project_url, data=self._get_prepared_data(), headers=self.headers),
            DateInFutureException,
            msg="test_business_id_exists",
        )

    def test_invalid_country_code(self):
        self.valid_data["company"]["country_code"] = "invalid"
        self._check_response(
            self.client.post(self.project_url, data=self._get_prepared_data(), headers=self.headers),
            InvalidCountryCodeException,
            msg="test_business_id_exists",
        )

    def test_country_code_not_found(self):
        self.valid_data["company"]["country_code"] = "AU"
        self._check_response(
            self.client.post(self.project_url, data=self._get_prepared_data(), headers=self.headers),
            CountryNotFoundException,
            msg="test_business_id_exists",
        )
