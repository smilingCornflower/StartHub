import time

from django.test import SimpleTestCase
from domain.enums.token import TokenTypeEnum
from domain.value_objects.auth_management.token import AccessPayload, AnonymousPayload, RefreshPayload


class TestAccessPayload(SimpleTestCase):
    def test_valid_payload(self):
        now = int(time.time())
        payload = AccessPayload(
            sub="user123",
            roles=["admin"],
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            iat=now,
            exp=now + 3600,
        )
        self.assertEqual(payload.type, TokenTypeEnum.ACCESS)

    def test_invalid_type(self):
        now = int(time.time())
        with self.assertRaises(ValueError):
            AccessPayload(
                sub="user123",
                roles=["admin"],
                email="test@example.com",
                first_name="John",
                last_name="Doe",
                iat=now,
                exp=now + 3600,
                type=TokenTypeEnum.REFRESH,
            )


class TestRefreshPayload(SimpleTestCase):
    def test_valid_payload(self):
        now = int(time.time())
        payload = RefreshPayload(sub="user123", iat=now, exp=now + 86400)
        self.assertEqual(payload.type, TokenTypeEnum.REFRESH)

    def test_invalid_type(self):
        now = int(time.time())
        with self.assertRaises(ValueError):
            RefreshPayload(sub="user123", iat=now, exp=now + 86400, type=TokenTypeEnum.ACCESS)


class TestAnonymousPayload(SimpleTestCase):
    def test_valid_payload(self):
        now = int(time.time())
        payload = AnonymousPayload(sub="anon123", iat=now, exp=now + 3600)
        self.assertEqual(payload.type, TokenTypeEnum.ANONYMOUS)

    def test_invalid_type(self):
        now = int(time.time())
        with self.assertRaises(ValueError):
            AnonymousPayload(sub="anon123", iat=now, exp=now + 3600, type=TokenTypeEnum.ACCESS)
