from django.test import TestCase
from domain.exceptions.user import EmailAlreadyExistsException, UsernameAlreadyExistsException
from domain.models.user import User
from domain.services.auth import RegistrationService
from domain.value_objects.user import Email, RawPassword, UserCreatePayload, Username
from infrastructure.repositories.user import DjUserReadRepository, DjUserWriteRepository


class TestRegistrationService(TestCase):
    service: RegistrationService

    @classmethod
    def setUpTestData(cls) -> None:
        cls.service = RegistrationService(DjUserReadRepository(), DjUserWriteRepository())

    def test_success_registration(self) -> None:
        payload = UserCreatePayload(
            username=Username("test"),
            email=Email("test@example.com"),
            password=RawPassword("Pass1234"),
        )
        self.service.register(payload)
        self.assertTrue(User.objects.filter(username="test").exists())

    def test_username_already_exists_register(self) -> None:
        User.objects.create_user(username="test", email="another.email@example.com", password="Pass1234")
        payload = UserCreatePayload(
            username=Username("test"),
            email=Email("test@example.com"),
            password=RawPassword("Pass1234"),
        )
        with self.assertRaises(UsernameAlreadyExistsException):
            self.service.register(payload)

    def test_email_already_exists_register(self) -> None:
        User.objects.create_user(username="another_username", email="test@example.com", password="Pass1234")
        payload = UserCreatePayload(
            username=Username("test"),
            email=Email("test@example.com"),
            password=RawPassword("Pass1234"),
        )
        with self.assertRaises(EmailAlreadyExistsException):
            self.service.register(payload)
