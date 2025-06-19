from datetime import UTC, datetime, timedelta

from django.test import TestCase
from domain.exceptions.auth import InvalidCredentialsException, TokenExpiredException
from domain.models.user import User
from domain.services.auth import AuthService, TokenService
from domain.value_objects.auth import LoginCredentials
from domain.value_objects.token import AccessTokenVo, RefreshTokenVo, TokenPairVo
from domain.value_objects.user import Email, RawPassword
from infrastructure.repositories.user import DjUserReadRepository, DjUserWriteRepository
from loguru import logger


class TestAuthService(TestCase):
    service: AuthService
    user_data: dict[str, str]

    @classmethod
    def setUpTestData(cls) -> None:
        cls.service = AuthService(TokenService(secret_key="secret"), DjUserReadRepository(), DjUserWriteRepository())
        cls.user_data = {
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "test@example.com",
            "password": "Pass1234",
        }
        user = User.objects.create_user(
            email=cls.user_data["email"],
            first_name=cls.user_data["first_name"],
            last_name=cls.user_data["last_name"],
            password=cls.user_data["password"],
        )
        cls.user_id = user.id

    def test_success_login(self) -> None:
        credentials = LoginCredentials(
            email=Email(value=self.user_data["email"]),
            password=RawPassword(value=self.user_data["password"]),
        )
        token_pair: TokenPairVo = self.service.login(credentials)
        user = User.objects.get(id=self.user_id)

        logger.debug(f"{user.last_login=}")
        self.assertTrue((user.last_login - datetime.now(UTC)) < timedelta(seconds=10))
        self.assertIsInstance(token_pair.access.value, str)
        self.assertIsInstance(token_pair.refresh.value, str)

    def test_login_with_invalid_credentials(self) -> None:
        credentials_1 = LoginCredentials(
            email=Email(value="not.existing@example.com"),
            password=RawPassword(value=self.user_data["password"]),
        )
        with self.assertRaises(InvalidCredentialsException):
            self.service.login(credentials_1)

        credentials_2 = LoginCredentials(
            email=Email(value=self.user_data["email"]),
            password=RawPassword(value="IncorrectPass1234"),
        )
        with self.assertRaises(InvalidCredentialsException):
            self.service.login(credentials_2)

    def test_success_reissue(self) -> None:
        credentials = LoginCredentials(
            email=Email(value=self.user_data["email"]),
            password=RawPassword(value=self.user_data["password"]),
        )
        token_pair: TokenPairVo = self.service.login(credentials)

        access_token: AccessTokenVo = self.service.reissue_access(token_pair.refresh)
        refresh_token: RefreshTokenVo = self.service.reissue_refresh(token_pair.refresh)
        self.assertIsInstance(access_token.value, str)
        self.assertIsInstance(refresh_token.value, str)

    def test_reissue_with_expired_token(self) -> None:
        auth_service = AuthService(
            TokenService(secret_key="secret", refresh_token_lifetime=-100),
            DjUserReadRepository(),
            DjUserWriteRepository(),
        )
        credentials = LoginCredentials(
            email=Email(value=self.user_data["email"]),
            password=RawPassword(value=self.user_data["password"]),
        )
        token_pair: TokenPairVo = auth_service.login(credentials)

        with self.assertRaises(TokenExpiredException):
            self.service.reissue_access(token_pair.refresh)

        with self.assertRaises(TokenExpiredException):
            self.service.reissue_refresh(token_pair.refresh)

    def test_protected_authenticate_user_with_correct_credentials(self) -> None:
        """:raises ValueError:"""
        credentials = LoginCredentials(
            email=Email(value=self.user_data["email"]),
            password=RawPassword(value=self.user_data["password"]),
        )
        user: User = self.service._authenticate_user(credentials)
        user_in_db: User | None = User.objects.filter(email=self.user_data["email"]).first()
        if user_in_db:
            self.assertEqual(user.first_name, user_in_db.first_name)
            self.assertEqual(user.last_name, user_in_db.last_name)
            self.assertEqual(user.email, user_in_db.email)
        else:
            raise ValueError("user_in_db is None")

    def test_protected_authenticate_user_with_invalid_credentials(self) -> None:
        with self.assertRaises(InvalidCredentialsException):
            credentials = LoginCredentials(
                email=Email(value="not.existing@example.com"),
                password=RawPassword(value=self.user_data["password"]),
            )
            self.service._authenticate_user(credentials)

        with self.assertRaises(InvalidCredentialsException):
            credentials = LoginCredentials(
                email=Email(value=self.user_data["email"]),
                password=RawPassword(value="IncorrectPass1234"),
            )
            self.service._authenticate_user(credentials)
