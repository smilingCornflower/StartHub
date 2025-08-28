from dataclasses import dataclass
from unittest.mock import Mock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase
from domain.value_objects.common import Description, FirstName, Id, LastName, PhoneNumber
from domain.value_objects.user_management.user import RawPassword, UserUpdateCommand
from presentation.request_converters.user_management.user import request_to_user_update_command


@dataclass
class ValidUserUpdateData:
    user_id = 123
    first_name = "John"
    last_name = "Doe"
    password = "NewPassword123!"
    description = "Updated user description"
    add_phone = "+77771234567"
    remove_phone = "+77779876543"
    profile_picture_content = b"fake image content"

    first_name_field = "first_name"
    last_name_field = "last_name"
    password_field = "password"
    description_field = "description"
    add_phone_field = "add_phone"
    remove_phone_field = "remove_phone"
    profile_picture_field = "profile_picture"

    def to_dict_with_all_fields(self):
        return {
            self.first_name_field: self.first_name,
            self.last_name_field: self.last_name,
            self.password_field: self.password,
            self.description_field: self.description,
            self.add_phone_field: self.add_phone,
            self.remove_phone_field: self.remove_phone,
        }

    def get_profile_picture_file(self):
        return SimpleUploadedFile(name="test.jpg", content=self.profile_picture_content, content_type="image/jpeg")


class TestRequestToUserUpdateCommand(SimpleTestCase):
    def setUp(self):
        self.data = ValidUserUpdateData()

    def apply_function(self, data, files, user_id):
        return request_to_user_update_command(data=data, files=files, user_id=user_id)

    def test_empty_data_and_files(self):
        data = {}
        files = {}

        expected = UserUpdateCommand(user_id=Id(value=self.data.user_id))

        result = self.apply_function(data, files, self.data.user_id)
        self.assertEqual(expected, result)

    def test_with_first_name_only(self):
        data = {self.data.first_name_field: self.data.first_name}
        files = {}

        expected = UserUpdateCommand(
            user_id=Id(value=self.data.user_id), first_name=FirstName(value=self.data.first_name)
        )

        result = self.apply_function(data, files, self.data.user_id)
        self.assertEqual(expected, result)

    def test_with_last_name_only(self):
        data = {self.data.last_name_field: self.data.last_name}
        files = {}

        expected = UserUpdateCommand(user_id=Id(value=self.data.user_id), last_name=LastName(value=self.data.last_name))

        result = self.apply_function(data, files, self.data.user_id)
        self.assertEqual(expected, result)

    def test_with_password_only(self):
        data = {self.data.password_field: self.data.password}
        files = {}

        expected = UserUpdateCommand(
            user_id=Id(value=self.data.user_id), password=RawPassword(value=self.data.password)
        )

        result = self.apply_function(data, files, self.data.user_id)
        self.assertEqual(expected, result)

    def test_with_description_only(self):
        data = {self.data.description_field: self.data.description}
        files = {}

        expected = UserUpdateCommand(
            user_id=Id(value=self.data.user_id), description=Description(value=self.data.description)
        )

        result = self.apply_function(data, files, self.data.user_id)
        self.assertEqual(expected, result)

    def test_with_add_phone_only(self):
        data = {self.data.add_phone_field: self.data.add_phone}
        files = {}

        expected = UserUpdateCommand(
            user_id=Id(value=self.data.user_id), add_phone=PhoneNumber(value=self.data.add_phone)
        )

        result = self.apply_function(data, files, self.data.user_id)
        self.assertEqual(expected, result)

    def test_with_remove_phone_only(self):
        data = {self.data.remove_phone_field: self.data.remove_phone}
        files = {}

        expected = UserUpdateCommand(
            user_id=Id(value=self.data.user_id), remove_phone=PhoneNumber(value=self.data.remove_phone)
        )

        result = self.apply_function(data, files, self.data.user_id)
        self.assertEqual(expected, result)

    def test_with_profile_picture_only(self):
        data = {}
        files = {self.data.profile_picture_field: self.data.get_profile_picture_file()}

        expected = UserUpdateCommand(
            user_id=Id(value=self.data.user_id), picture_data=self.data.profile_picture_content
        )

        result = self.apply_function(data, files, self.data.user_id)
        self.assertEqual(expected, result)

    def test_with_all_fields_and_file(self):
        data = self.data.to_dict_with_all_fields()
        files = {self.data.profile_picture_field: self.data.get_profile_picture_file()}

        expected = UserUpdateCommand(
            user_id=Id(value=self.data.user_id),
            first_name=FirstName(value=self.data.first_name),
            last_name=LastName(value=self.data.last_name),
            password=RawPassword(value=self.data.password),
            description=Description(value=self.data.description),
            add_phone=PhoneNumber(value=self.data.add_phone),
            remove_phone=PhoneNumber(value=self.data.remove_phone),
            picture_data=self.data.profile_picture_content,
        )
        result = self.apply_function(data, files, self.data.user_id)
        self.assertEqual(expected, result)
