from dataclasses import asdict
from datetime import datetime
from unittest.mock import Mock

import jwt
from django.test import SimpleTestCase
from domain.constants import JWT_ALGORITHM
from domain.enums.token import TokenTypeEnum
from domain.exceptions.auth import InvalidTokenException, TokenExpiredException
from domain.services.auth import TokenService
from domain.value_objects.auth_management.token import (
    AccessPayload,
    AccessTokenVo,
    AnonymousPayload,
    AnonymousTokenVo,
    RefreshPayload,
    RefreshTokenVo,
)
from tests.common.check_raises import check_raises


class TestTokenService(SimpleTestCase):
    SECRET_KEY = "secret"
    ACCESS_LIFETIME = REFRESH_LIFETIME = ANONYMOUS_LIFETIME = 3600
    TIME_TOLERANCE_IN_SECONDS = 5

    def setUp(self):
        self.mock_user = self._create_mock_user()
        self.mock_role = self._create_mock_role()
        self.service = self._create_service()

    def _create_mock_user(self):
        user = Mock()
        user.id = 1
        user.email = "test@example.com"
        user.first_name = "first_name"
        user.last_name = "last_name"
        return user

    def _create_mock_role(self):
        role = Mock()
        role.name = "admin"
        return role

    def _create_service(self, **overrides):
        mock_role_repository = Mock()
        mock_role_repository.get_all.return_value = [self.mock_role]

        defaults = {
            "role_read_repository": mock_role_repository,
            "secret_key": self.SECRET_KEY,
            "access_token_lifetime": self.ACCESS_LIFETIME,
            "refresh_token_lifetime": self.REFRESH_LIFETIME,
            "anonymous_token_lifetime": self.ANONYMOUS_LIFETIME,
        }
        defaults.update(overrides)
        return TokenService(**defaults)

    def _decode_token(self, token):
        return jwt.decode(token, self.SECRET_KEY, algorithms=[JWT_ALGORITHM])

    def _assert_timestamp_valid(self, timestamp, expected_offset=0):
        now = datetime.now()
        expected = now.timestamp() + expected_offset
        self.assertLess(abs(timestamp - expected), self.TIME_TOLERANCE_IN_SECONDS)

    def _assert_payload_matches(self, payload, expected_fields, lifetime):
        for key, value in expected_fields.items():
            self.assertEqual(payload[key], value)
        self._assert_timestamp_valid(payload["iat"])
        self._assert_timestamp_valid(payload["exp"], lifetime)

    def _get_expected_access_fields(self):
        return {
            "sub": str(self.mock_user.id),
            "roles": [self.mock_role.name],
            "email": self.mock_user.email,
            "first_name": self.mock_user.first_name,
            "last_name": self.mock_user.last_name,
            "type": TokenTypeEnum.ACCESS,
        }

    def _get_expected_refresh_fields(self):
        return {"sub": str(self.mock_user.id), "type": TokenTypeEnum.REFRESH}

    def _assert_exception_raised(self, method, token, exception_class):
        check_raises(method, exception_class)
        with self.assertRaises(exception_class):
            method(token)

    def test_generate_access_token(self):
        token = self.service.generate_access(user=self.mock_user)
        payload = self._decode_token(token.value)
        self._assert_payload_matches(payload, self._get_expected_access_fields(), self.ACCESS_LIFETIME)

    def test_generate_refresh_token(self):
        token = self.service.generate_refresh(user=self.mock_user)
        payload = self._decode_token(token.value)
        self._assert_payload_matches(payload, self._get_expected_refresh_fields(), self.REFRESH_LIFETIME)

    def test_generate_anonymous_token(self):
        token = self.service.generate_anonymous()
        payload = self._decode_token(token.value)
        expected_fields = {"sub": payload["sub"], "type": TokenTypeEnum.ANONYMOUS}
        self._assert_payload_matches(payload, expected_fields, self.ANONYMOUS_LIFETIME)

    def test_verify_access_with_valid_token(self):
        token = self.service.generate_access(self.mock_user)
        access_payload = self.service.verify_access(token=token)

        self.assertIsInstance(access_payload, AccessPayload)
        self._assert_payload_matches(asdict(access_payload), self._get_expected_access_fields(), self.ACCESS_LIFETIME)

    def test_verify_access_with_invalid_token(self):
        token = AccessTokenVo(value="INVALID")
        self._assert_exception_raised(self.service.verify_access, token, InvalidTokenException)

    def test_verify_access_with_not_access_token(self):
        refresh_token = self.service.generate_refresh(self.mock_user)
        with self.assertRaises(InvalidTokenException):
            self.service.verify_access(refresh_token)

    def test_verify_access_with_expired_token(self):
        expired_service = self._create_service(access_token_lifetime=-100)
        expired_token = expired_service.generate_access(self.mock_user)
        self._assert_exception_raised(self.service.verify_access, expired_token, TokenExpiredException)

    def test_verify_refresh_with_valid_token(self):
        token = self.service.generate_refresh(user=self.mock_user)
        refresh_payload = self.service.verify_refresh(token)

        self.assertIsInstance(refresh_payload, RefreshPayload)
        self._assert_payload_matches(
            asdict(refresh_payload), self._get_expected_refresh_fields(), self.REFRESH_LIFETIME
        )

    def test_verify_refresh_with_invalid_token(self):
        token = RefreshTokenVo(value="INVALID")
        self._assert_exception_raised(self.service.verify_refresh, token, InvalidTokenException)

    def test_verify_refresh_with_not_refresh_token(self):
        access_token = self.service.generate_access(user=self.mock_user)
        with self.assertRaises(InvalidTokenException):
            self.service.verify_refresh(access_token)

    def test_verify_refresh_with_expired_token(self):
        expired_service = self._create_service(refresh_token_lifetime=-100)
        expired_token = expired_service.generate_refresh(user=self.mock_user)
        self._assert_exception_raised(self.service.verify_refresh, expired_token, TokenExpiredException)

    def test_verify_anonymous_with_valid_token(self):
        token = self.service.generate_anonymous()
        anonymous_payload = self.service.verify_anonymous(token)

        self.assertIsInstance(anonymous_payload, AnonymousPayload)
        expected = {"sub": anonymous_payload.sub, "type": TokenTypeEnum.ANONYMOUS}
        self._assert_payload_matches(asdict(anonymous_payload), expected, self.ANONYMOUS_LIFETIME)

    def test_verify_anonymous_with_invalid_token(self):
        token = AnonymousTokenVo(value="INVALID")
        self._assert_exception_raised(self.service.verify_anonymous, token, InvalidTokenException)

    def test_verify_anonymous_with_expired_token(self):
        expired_service = self._create_service(anonymous_token_lifetime=-100)
        expired_token = expired_service.generate_anonymous()
        self._assert_exception_raised(self.service.verify_anonymous, expired_token, TokenExpiredException)
