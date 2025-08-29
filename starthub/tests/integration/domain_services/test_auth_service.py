from application.builders.domain_service.auth import AuthServiceBuilder, TokenServiceBuilder
from django.test import TestCase
from domain.exceptions.auth import InvalidCredentialsException, InvalidTokenException
from domain.models.user_management.user import User
from domain.value_objects.auth_management.auth import LoginCredentials
from domain.value_objects.auth_management.token import AccessTokenVo, RefreshTokenVo, TokenPairVo
from domain.value_objects.user_management.user import Email, RawPassword


class TestAuthService(TestCase):
    EMAIL = "test@email.com"
    NONEXISTENT_EMAIL = "nonexistent@email.com"
    VALID_PASSWORD = "Password123!"
    INVALID_PASSWORD = "Invalid123!"

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email=cls.EMAIL, password=cls.VALID_PASSWORD)

    def setUp(self):
        self.auth_service = AuthServiceBuilder.create_service()
        self.token_service = TokenServiceBuilder.create_service()

    def _create_credentials(self, email=None, password=None):
        return LoginCredentials(
            email=Email(value=email or self.EMAIL), password=RawPassword(value=password or self.VALID_PASSWORD)
        )

    def test_login_with_valid_credentials(self):
        last_login_before = self.user.last_login
        credentials = self._create_credentials()

        token_pair = self.auth_service.login(credentials)

        self.assertIsInstance(token_pair, TokenPairVo)
        access_payload = self.token_service.verify_access(token_pair.access)
        self.assertEqual(access_payload.email, self.user.email)

        updated_user = User.objects.get(email=self.user.email)
        self.assertNotEqual(last_login_before, updated_user.last_login)

    def test_login_with_invalid_password(self):
        credentials = self._create_credentials(password=self.INVALID_PASSWORD)
        with self.assertRaises(InvalidCredentialsException):
            self.auth_service.login(credentials)

    def test_login_with_nonexistent_email(self):
        credentials = self._create_credentials(email=self.NONEXISTENT_EMAIL)
        with self.assertRaises(InvalidCredentialsException):
            self.auth_service.login(credentials)

    def test_reissue_access_success(self):
        credentials = self._create_credentials()
        token_pair = self.auth_service.login(credentials)

        access_token = self.auth_service.reissue_access(token_pair.refresh)

        self.assertIsInstance(access_token, AccessTokenVo)

    def test_reissue_access_failure(self):
        invalid_token = RefreshTokenVo(value="INVALID")
        with self.assertRaises(InvalidTokenException):
            self.auth_service.reissue_access(invalid_token)

    def test_reissue_refresh_success(self):
        credentials = self._create_credentials()
        token_pair = self.auth_service.login(credentials)

        refresh_token = self.auth_service.reissue_refresh(token_pair.refresh)

        self.assertIsInstance(refresh_token, RefreshTokenVo)

    def test_reissue_refresh_failure(self):
        invalid_token = RefreshTokenVo(value="INVALID")
        with self.assertRaises(InvalidTokenException):
            self.auth_service.reissue_refresh(invalid_token)
