from datetime import UTC, datetime
from typing import cast
from unittest.mock import MagicMock

import jwt
from django.test import TestCase
from domain.constants import ACCESS_TOKEN_LIFETIME, JWT_ALGORITHM, REFRESH_TOKEN_LIFETIME
from domain.enums.token import TokenTypeEnum
from domain.exceptions.auth import InvalidTokenException, TokenExpiredException
from domain.models.user import User
from domain.services.token import TokenService
from domain.value_objects.token import AccessPayload, AccessTokenVo, RefreshPayload, RefreshTokenVo
from loguru import logger


class TokenServiceTestCase(TestCase):
    secret_key: str
    token_service: TokenService
    token_service_with_invalid_key: TokenService
    user: User
    access_token_lifetime: int
    refresh_token_lifetime: int
    invalid_secret: str

    @classmethod
    def setUpTestData(cls) -> None:
        cls.secret_key = "secret_key"
        cls.invalid_secret = "invalid_key"
        cls.access_token_lifetime = ACCESS_TOKEN_LIFETIME
        cls.refresh_token_lifetime = REFRESH_TOKEN_LIFETIME

        cls.token_service = TokenService(
            secret_key=cls.secret_key,
            access_token_lifetime=cls.access_token_lifetime,
            refresh_token_lifetime=cls.refresh_token_lifetime,
        )
        cls.token_service_with_invalid_key = TokenService(
            secret_key=cls.invalid_secret,
            access_token_lifetime=cls.access_token_lifetime,
            refresh_token_lifetime=cls.refresh_token_lifetime,
        )
        mock_user = MagicMock(spec=User)
        mock_user.id = 1
        mock_user.email = "test@example.com"
        mock_user.first_name = "first_name"
        mock_user.last_name = "last_name"

        cls.user = mock_user

    def test_generate_access_token(self) -> None:
        access_token: AccessTokenVo = self.token_service.generate_access(user=self.user)

        self.assertIsInstance(access_token, AccessTokenVo)
        self.assertTrue(access_token.value)
        logger.debug(f"{access_token.value=}")
        decoded_payload: dict[str, int | str] = jwt.decode(
            access_token.value, self.secret_key, algorithms=[JWT_ALGORITHM]
        )
        logger.debug(f"decoded access payload = {decoded_payload}")

        self.check_iat(cast(int, decoded_payload["iat"]))
        self.check_exp(cast(int, decoded_payload["exp"]), self.access_token_lifetime)

        self.assertEqual(decoded_payload["sub"], str(self.user.id))
        self.assertEqual(decoded_payload["email"], self.user.email)
        self.assertEqual(decoded_payload["type"], TokenTypeEnum.ACCESS)

    def test_generate_refresh_token(self) -> None:
        refresh_token: RefreshTokenVo = self.token_service.generate_refresh(user=self.user)

        self.assertIsInstance(refresh_token, RefreshTokenVo)
        self.assertTrue(refresh_token.value)

        decoded_payload = jwt.decode(refresh_token.value, self.secret_key, algorithms=[JWT_ALGORITHM])
        logger.debug(f"decoded refresh payload = {decoded_payload}")

        self.check_iat(cast(int, decoded_payload["iat"]))
        self.check_exp(cast(int, decoded_payload["exp"]), self.refresh_token_lifetime)

        self.assertEqual(decoded_payload["sub"], str(self.user.id))
        self.assertEqual(decoded_payload["type"], TokenTypeEnum.REFRESH)

    def test_verify_valid_access_token(self) -> None:
        access_token: AccessTokenVo = self.token_service.generate_access(self.user)
        access_payload: AccessPayload = self.token_service.verify_access(access_token)
        self.assertIsInstance(access_payload, AccessPayload)

        self.check_iat(access_payload.iat)
        self.check_exp(access_payload.exp, self.access_token_lifetime)

        self.assertEqual(access_payload.sub, str(self.user.id))
        self.assertEqual(access_payload.email, self.user.email)
        self.assertEqual(access_payload.type, TokenTypeEnum.ACCESS)

    def test_verify_valid_refresh_token(self) -> None:
        refresh_token: RefreshTokenVo = self.token_service.generate_refresh(self.user)
        refresh_payload: RefreshPayload = self.token_service.verify_refresh(refresh_token)
        self.assertIsInstance(refresh_payload, RefreshPayload)

        self.check_iat(refresh_payload.iat)
        self.check_exp(refresh_payload.exp, self.refresh_token_lifetime)

        self.assertEqual(refresh_payload.sub, str(self.user.id))
        self.assertEqual(refresh_payload.type, TokenTypeEnum.REFRESH)

    def test_access_token_with_wrong_secret(self) -> None:
        access_token: AccessTokenVo = self.token_service_with_invalid_key.generate_access(self.user)
        with self.assertRaises(InvalidTokenException) as context:
            self.token_service.verify_access(access_token)
        self.assertEqual(str(context.exception), "Invalid access token.")

    def test_refresh_token_with_wrong_secret(self) -> None:
        refresh_token: RefreshTokenVo = self.token_service_with_invalid_key.generate_refresh(self.user)
        with self.assertRaises(InvalidTokenException) as context:
            self.token_service.verify_refresh(refresh_token)
        self.assertEqual(str(context.exception), "Invalid refresh token.")

    def test_expired_access_token(self) -> None:
        iat = int((datetime.now(UTC)).timestamp()) - 100
        exp = iat + 1

        payload = {
            "sub": str(self.user.id),
            "email": self.user.email,
            "iat": iat,
            "exp": exp,
            "type": TokenTypeEnum.ACCESS,
        }
        expired_token: str = jwt.encode(payload, self.secret_key, algorithm=JWT_ALGORITHM)
        with self.assertRaises(TokenExpiredException) as context:
            self.token_service.verify_access(AccessTokenVo(value=expired_token))
        self.assertEqual(str(context.exception), "Access token has expired.")

    def test_expired_refresh_token(self) -> None:
        iat = int((datetime.now(UTC)).timestamp()) - 100
        exp = iat + 1

        payload = {
            "sub": str(self.user.id),
            "email": self.user.email,
            "iat": iat,
            "exp": exp,
            "type": TokenTypeEnum.REFRESH,
        }
        expired_token: str = jwt.encode(payload, self.secret_key, algorithm=JWT_ALGORITHM)
        with self.assertRaises(TokenExpiredException) as context:
            self.token_service.verify_refresh(RefreshTokenVo(value=expired_token))
        self.assertEqual(str(context.exception), "Refresh token has expired.")

    def test_access_token_with_missing_fields(self) -> None:
        iat = int(datetime.now(UTC).timestamp())
        exp = iat + self.access_token_lifetime

        base_payload = {
            "sub": str(self.user.id),
            "email": self.user.email,
            "iat": iat,
            "exp": exp,
            "type": TokenTypeEnum.ACCESS,
        }
        for missing_field in base_payload.keys():
            with self.subTest(missing_field=missing_field):
                invalid_payload = {k: v for k, v in base_payload.items() if k != missing_field}
                token_str = jwt.encode(invalid_payload, self.secret_key, algorithm=JWT_ALGORITHM)

                with self.assertRaises(InvalidTokenException) as context:
                    self.token_service.verify_access(AccessTokenVo(value=token_str))
                self.assertEqual(str(context.exception), "Invalid access token.")

    def test_refresh_token_with_missing_fields(self) -> None:
        iat = int(datetime.now(UTC).timestamp())
        exp = iat + self.refresh_token_lifetime

        base_payload = {
            "sub": str(self.user.id),
            "iat": iat,
            "exp": exp,
            "type": TokenTypeEnum.REFRESH,
        }
        for missing_field in base_payload.keys():
            with self.subTest(missing_field=missing_field):
                invalid_payload = {k: v for k, v in base_payload.items() if k != missing_field}
                token_str = jwt.encode(invalid_payload, self.secret_key, algorithm=JWT_ALGORITHM)

                with self.assertRaises(InvalidTokenException) as context:
                    self.token_service.verify_refresh(RefreshTokenVo(value=token_str))
                self.assertEqual(str(context.exception), "Invalid refresh token.")

    def test_token_with_str_exp(self) -> None:
        """
        Verifies that a token with expired 'exp' (even as string)
        raises TokenExpiredException.
        """
        iat = int(datetime.now(UTC).timestamp()) - 200
        exp = iat + 100

        payload = {
            "sub": str(self.user.id),
            "iat": str(iat),
            "exp": str(exp),
            "type": TokenTypeEnum.ACCESS,
        }
        token_str = jwt.encode(payload, self.secret_key, algorithm=JWT_ALGORITHM)
        with self.assertRaises(TokenExpiredException):
            self.token_service.verify_refresh(RefreshTokenVo(value=token_str))

    def test_token_with_str_iat(self) -> None:
        """
        Verifies that a token with 'iat' set in the future (even as string)
        raises InvalidTokenException.
        """
        iat = int(datetime.now(UTC).timestamp()) + 100
        exp = iat + self.refresh_token_lifetime + 200

        payload = {
            "sub": str(self.user.id),
            "iat": str(iat),
            "exp": str(exp),
            "type": TokenTypeEnum.REFRESH,
        }
        token_str = jwt.encode(payload, self.secret_key, algorithm=JWT_ALGORITHM)
        with self.assertRaises(InvalidTokenException):
            self.token_service.verify_refresh(RefreshTokenVo(value=token_str))

    def test_protected_verify_access_invalid_type(self) -> None:
        """
        _verify_access raises ValueError when type != 'access'
        """
        iat = int(datetime.now(UTC).timestamp())
        exp = iat + self.access_token_lifetime
        payload = {
            "sub": str(self.user.id),
            "email": self.user.email,
            "iat": iat,
            "exp": exp,
            "type": "invalid",
        }
        token_str = jwt.encode(payload, self.secret_key, algorithm=JWT_ALGORITHM)
        with self.assertRaises(ValueError):
            self.token_service._verify_access(AccessTokenVo(value=token_str))

    def test_protected_verify_refresh_invalid_type(self) -> None:
        """
        _verify_refresh raises ValueError, when type != 'refresh'
        """
        iat = int(datetime.now(UTC).timestamp())
        exp = iat + self.refresh_token_lifetime
        payload = {
            "sub": str(self.user.id),
            "iat": iat,
            "exp": exp,
            "type": "invalid",
        }
        token_str = jwt.encode(payload, self.secret_key, algorithm=JWT_ALGORITHM)
        with self.assertRaises(ValueError):
            self.token_service._verify_refresh(RefreshTokenVo(value=token_str))

    def test_protected_verify_access_missing_required_field(self) -> None:
        """
        _verify_access raises KeyError when required field is missing.
        """
        iat = int(datetime.now(UTC).timestamp())
        exp = iat + self.access_token_lifetime

        # missing email
        payload = {
            "sub": str(self.user.id),
            "iat": iat,
            "exp": exp,
            "type": TokenTypeEnum.ACCESS,
        }
        token_str = jwt.encode(payload, self.secret_key, algorithm=JWT_ALGORITHM)
        with self.assertRaises(jwt.PyJWTError):
            self.token_service._verify_access(AccessTokenVo(value=token_str))

    def test_protected_verify_refresh_missing_required_field(self) -> None:
        """
        _verify_refresh raises KeyError when required field is missing.
        """
        iat = int(datetime.now(UTC).timestamp())

        # missing exp
        payload = {
            "sub": str(self.user.id),
            "iat": iat,
            "type": TokenTypeEnum.REFRESH,
        }
        token_str = jwt.encode(payload, self.secret_key, algorithm=JWT_ALGORITHM)
        with self.assertRaises(jwt.PyJWTError):
            self.token_service._verify_refresh(RefreshTokenVo(value=token_str))

    def test_verify_token_generated_with_negative_lifetime_service(self) -> None:
        token_service = TokenService(secret_key=self.secret_key, refresh_token_lifetime=-60)
        refresh_token_vo = token_service.generate_refresh(self.user)

        with self.assertRaises(TokenExpiredException):
            token_service.verify_refresh(refresh_token_vo)

    def check_iat(self, iat: int) -> None:
        now: float = datetime.now(UTC).timestamp()
        self.assertLess(abs(now - iat), 3)

    def check_exp(self, exp: int, lifetime: int) -> None:
        now: float = datetime.now(UTC).timestamp()
        self.assertLess(abs(now + lifetime - exp), 3)
