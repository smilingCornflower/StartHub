from application.builders.domain_service.auth import RegistrationServiceBuilder
from django.test import TestCase
from domain.exceptions.user import EmailAlreadyExistsException
from domain.models.user_management.user import User
from domain.value_objects.user_management.user import Email, RawPassword, UserCreatePayload
from tests.common.check_raises import check_raises_in_docs


class TestRegistrationService(TestCase):
    EMAIL = "test@example.com"
    EXISTING_EMAIL = "existing@example.com"
    PASSWORD = "Password123!"

    def setUp(self):
        self.service = RegistrationServiceBuilder.create_service()

    def _create_payload(self, email=None):
        return UserCreatePayload(email=Email(value=email or self.EMAIL), password=RawPassword(value=self.PASSWORD))

    def test_register_successfully(self):
        user = self.service.register(self._create_payload())

        self.assertEqual(user.email, self.EMAIL)
        self.assertTrue(User.objects.filter(email=self.EMAIL).exists())

    def test_register_with_existing_email_raises_exception(self):
        User.objects.create_user(email=self.EXISTING_EMAIL, password=self.PASSWORD)
        payload = self._create_payload(email=self.EXISTING_EMAIL)

        check_raises_in_docs(self.service.register, EmailAlreadyExistsException)
        with self.assertRaises(EmailAlreadyExistsException):
            self.service.register(payload)
