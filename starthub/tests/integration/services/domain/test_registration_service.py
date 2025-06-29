from django.test import TestCase
from domain.exceptions.user import EmailAlreadyExistsException
from domain.models.user import User
from domain.services.auth import RegistrationService
from domain.value_objects.common import FirstName, LastName
from domain.value_objects.user import Email, RawPassword, UserCreatePayload
from infrastructure.repositories.user import DjUserReadRepository, DjUserWriteRepository


class TestRegistrationService(TestCase):
    service: RegistrationService

    @classmethod
    def setUpTestData(cls) -> None:
        cls.service = RegistrationService(DjUserReadRepository(), DjUserWriteRepository())

    def test_success_registration(self) -> None:
        payload = UserCreatePayload(
            email=Email(value="test@example.com"),
            password=RawPassword(value="Pass1234"),
        )
        self.service.register(payload)
        self.assertTrue(User.objects.filter(email="test@example.com").exists())

    def test_email_already_exists_register(self) -> None:
        User.objects.create_user(
            first_name="first_name", last_name="last_name", email="test@example.com", password="Pass1234"
        )
        payload = UserCreatePayload(
            email=Email(value="test@example.com"),
            password=RawPassword(value="Pass1234"),
        )
        with self.assertRaises(EmailAlreadyExistsException):
            self.service.register(payload)
