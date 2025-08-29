from dataclasses import dataclass
from unittest.mock import Mock

from django.test import SimpleTestCase
from domain.enums.role import RoleEnum
from domain.exceptions.validation import ValidationException
from domain.value_objects.user_management.user_admin import UserAdminUpdateCommand
from presentation.request_converters.user_management.user_admin import request_to_user_admin_update_command
from rest_framework.request import Request
from tests.common.check_raises import check_raises


@dataclass
class ValidUserAdminUpdateData:
    role = "admin"

    add_role_field = "add_role"
    remove_role_field = "remove_role"

    def to_dict_with_add_role(self):
        return {
            self.add_role_field: self.role,
        }

    def to_dict_with_remove_role(self):
        return {
            self.remove_role_field: self.role,
        }

    def to_dict_with_both_roles(self):
        return {
            self.add_role_field: self.role,
            self.remove_role_field: self.role,
        }


class TestRequestToUserAdminUpdateCommand(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidUserAdminUpdateData()

    def test_no_data(self):
        request = Mock(spec=Request)
        request.data = {}

        expected = UserAdminUpdateCommand(
            add_role=None,
            remove_role=None,
        )

        result = request_to_user_admin_update_command(request)
        self.assertEqual(expected, result)

    def test_add_role_only(self):
        request = Mock(spec=Request)
        request.data = self.valid_dataclass.to_dict_with_add_role()

        expected = UserAdminUpdateCommand(
            add_role=RoleEnum(value=self.valid_dataclass.role),
            remove_role=None,
        )

        result = request_to_user_admin_update_command(request)
        self.assertEqual(expected, result)

    def test_remove_role_only(self):
        request = Mock(spec=Request)
        request.data = self.valid_dataclass.to_dict_with_remove_role()

        expected = UserAdminUpdateCommand(
            add_role=None,
            remove_role=RoleEnum(value=self.valid_dataclass.role),
        )

        result = request_to_user_admin_update_command(request)
        self.assertEqual(expected, result)

    def test_both_roles(self):
        request = Mock(spec=Request)
        request.data = self.valid_dataclass.to_dict_with_both_roles()

        expected = UserAdminUpdateCommand(
            add_role=RoleEnum(value=self.valid_dataclass.role),
            remove_role=RoleEnum(value=self.valid_dataclass.role),
        )

        result = request_to_user_admin_update_command(request)
        self.assertEqual(expected, result)

    def test_invalid_add_role(self):
        request = Mock(spec=Request)
        request.data = {self.valid_dataclass.add_role_field: "invalid_role"}

        exc = ValidationException
        with self.assertRaises(exc):
            request_to_user_admin_update_command(request)
        check_raises(request_to_user_admin_update_command, exc)

    def test_invalid_remove_role(self):
        request = Mock(spec=Request)
        request.data = {self.valid_dataclass.remove_role_field: "invalid_role"}

        exc = ValidationException
        with self.assertRaises(exc):
            request_to_user_admin_update_command(request)
        check_raises(request_to_user_admin_update_command, exc)
