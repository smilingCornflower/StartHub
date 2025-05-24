from django.test import TestCase
from domain.exceptions.auth import InvalidCredentialsException, TokenExpiredException
from domain.models.user import User
from domain.services.auth import AuthService
from domain.services.token import TokenService
from domain.value_objects.auth import LoginCredentials
from domain.value_objects.token import AccessTokenVo, RefreshTokenVo, TokenPairVo
from domain.value_objects.user import Email, RawPassword
from infrastructure.repositories.user import DjUserReadRepository


class TestAuthService(TestCase):
    service: AuthService
    user_data: dict[str, str]

    @classmethod
    def setUpTestData(cls) -> None:
        cls.service = AuthService(TokenService(secret_key="secret"), DjUserReadRepository())
        cls.user_data = {
            "username": "test",
            "email": "test@example.com",
            "password": "Pass1234",
        }
        User.objects.create_user(
            username=cls.user_data["username"],
            email=cls.user_data["email"],
            password=cls.user_data["password"],
        )

    def test_success_login(self) -> None:
        credentials = LoginCredentials(
            email=Email(self.user_data["email"]),
            password=RawPassword(self.user_data["password"]),
        )
        token_pair: TokenPairVo = self.service.login(credentials)

        self.assertIsInstance(token_pair.access.value, str)
        self.assertIsInstance(token_pair.refresh.value, str)

    def test_login_with_invalid_credentials(self) -> None:
        credentials_1 = LoginCredentials(
            email=Email("not.existing@example.com"),
            password=RawPassword(self.user_data["password"]),
        )
        with self.assertRaises(InvalidCredentialsException):
            self.service.login(credentials_1)

        credentials_2 = LoginCredentials(
            email=Email(self.user_data["email"]),
            password=RawPassword("IncorrectPass1234"),
        )
        with self.assertRaises(InvalidCredentialsException):
            self.service.login(credentials_2)

    def test_success_reissue(self) -> None:
        credentials = LoginCredentials(
            email=Email(self.user_data["email"]),
            password=RawPassword(self.user_data["password"]),
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
        )
        credentials = LoginCredentials(
            email=Email(self.user_data["email"]),
            password=RawPassword(self.user_data["password"]),
        )
        token_pair: TokenPairVo = auth_service.login(credentials)

        with self.assertRaises(TokenExpiredException):
            self.service.reissue_access(token_pair.refresh)

        with self.assertRaises(TokenExpiredException):
            self.service.reissue_refresh(token_pair.refresh)

    def test_protected_authenticate_user_with_correct_credentials(self) -> None:
        credentials = LoginCredentials(
            email=Email(self.user_data["email"]),
            password=RawPassword(self.user_data["password"]),
        )
        user: User = self.service._authenticate_user(credentials)
        user_in_db: User | None = User.objects.filter(email=self.user_data["email"]).first()
        if user_in_db:
            self.assertEqual(user.username, user_in_db.username)
            self.assertEqual(user.email, user_in_db.email)
        else:
            raise ValueError("user_in_db is None")

    def test_protected_authenticate_user_with_invalid_credentials(self) -> None:
        with self.assertRaises(InvalidCredentialsException):
            credentials = LoginCredentials(
                email=Email("not.existing@example.com"),
                password=RawPassword(self.user_data["password"]),
            )
            self.service._authenticate_user(credentials)

        with self.assertRaises(InvalidCredentialsException):
            credentials = LoginCredentials(
                email=Email(self.user_data["email"]),
                password=RawPassword("IncorrectPass1234"),
            )
            self.service._authenticate_user(credentials)
