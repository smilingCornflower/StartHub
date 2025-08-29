from dataclasses import dataclass
from unittest.mock import Mock

from django.test import SimpleTestCase
from domain.exceptions.validation import MissingRequiredFieldException, ValidationException
from domain.value_objects.common import FirstName, LastName, PhoneNumber
from domain.value_objects.user_management.user import Email
from domain.value_objects.user_management.user_message import (
    UserMessageContent,
    UserMessageCreateCommand,
    UserMessageTopic,
)
from presentation.request_converters.user_management.user_message import request_to_user_message_create_command
from rest_framework.request import Request


@dataclass
class ValidUserMessageData:
    first_name = "John"
    last_name = "Doe"
    email = "john.doe@example.com"
    phone = "+77771234567"
    topic = "Support"
    content = "Test message content"

    first_name_field = "first_name"
    last_name_field = "last_name"
    email_field = "email"
    phone_field = "phone"
    topic_field = "topic"
    content_field = "content"

    def to_dict(self):
        return {
            self.first_name_field: self.first_name,
            self.last_name_field: self.last_name,
            self.email_field: self.email,
            self.phone_field: self.phone,
            self.topic_field: self.topic,
            self.content_field: self.content,
        }


class TestRequestToUserMessageCreateCommand(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidUserMessageData()

    def test_valid_data_with_all_fields(self):
        request = Mock(spec=Request)
        request.data = self.valid_dataclass.to_dict()

        expected = UserMessageCreateCommand(
            first_name=FirstName(value=self.valid_dataclass.first_name),
            last_name=LastName(value=self.valid_dataclass.last_name),
            email=Email(value=self.valid_dataclass.email),
            phone=PhoneNumber(value=self.valid_dataclass.phone),
            topic=UserMessageTopic(value=self.valid_dataclass.topic),
            content=UserMessageContent(value=self.valid_dataclass.content),
        )

        result = request_to_user_message_create_command(request)
        self.assertEqual(expected, result)

    def test_missing_first_name(self):
        request = Mock(spec=Request)
        data = self.valid_dataclass.to_dict()
        del data[self.valid_dataclass.first_name_field]
        request.data = data

        with self.assertRaises(MissingRequiredFieldException):
            request_to_user_message_create_command(request)

    def test_missing_last_name(self):
        request = Mock(spec=Request)
        data = self.valid_dataclass.to_dict()
        del data[self.valid_dataclass.last_name_field]
        request.data = data

        with self.assertRaises(MissingRequiredFieldException):
            request_to_user_message_create_command(request)

    def test_missing_email(self):
        request = Mock(spec=Request)
        data = self.valid_dataclass.to_dict()
        del data[self.valid_dataclass.email_field]
        request.data = data

        with self.assertRaises(MissingRequiredFieldException):
            request_to_user_message_create_command(request)

    def test_missing_phone(self):
        request = Mock(spec=Request)
        data = self.valid_dataclass.to_dict()
        del data[self.valid_dataclass.phone_field]
        request.data = data

        with self.assertRaises(MissingRequiredFieldException):
            request_to_user_message_create_command(request)

    def test_missing_topic(self):
        request = Mock(spec=Request)
        data = self.valid_dataclass.to_dict()
        del data[self.valid_dataclass.topic_field]
        request.data = data

        with self.assertRaises(MissingRequiredFieldException):
            request_to_user_message_create_command(request)

    def test_missing_content(self):
        request = Mock(spec=Request)
        data = self.valid_dataclass.to_dict()
        del data[self.valid_dataclass.content_field]
        request.data = data

        with self.assertRaises(MissingRequiredFieldException):
            request_to_user_message_create_command(request)
