import pydantic
from django.test import SimpleTestCase
from domain.value_objects.user_management.user import PermissionVo


class TestPermissionVo(SimpleTestCase):
    def test_valid_3_parts(self):
        val = "view.own.user"
        permission = PermissionVo(value=val)
        self.assertEqual(permission.value, val)

    def test_valid_4_parts(self):
        val = "view.own.user.name"
        permission = PermissionVo(value=val)
        self.assertEqual(permission.value, val)

    def test_valid_5_parts(self):
        val = "view.own.user.name.john"
        permission = PermissionVo(value=val)
        self.assertEqual(permission.value, val)

    def test_invalid_parts_count(self):
        with self.assertRaises(pydantic.ValidationError):
            PermissionVo(value="view.own")

    def test_invalid_action(self):
        with self.assertRaises(pydantic.ValidationError):
            PermissionVo(value="INVALID.own.user")

    def test_invalid_scope(self):
        with self.assertRaises(pydantic.ValidationError):
            PermissionVo(value="view.INVALID.user")

    def test_invalid_model_format(self):
        with self.assertRaises(pydantic.ValidationError):
            PermissionVo(value="view.own.User")

    def test_invalid_field(self):
        with self.assertRaises(pydantic.ValidationError):
            PermissionVo(value="view.own.user.INVALID")
