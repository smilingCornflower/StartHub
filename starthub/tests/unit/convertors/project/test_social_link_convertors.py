from dataclasses import dataclass
from unittest.mock import Mock

from django.test import SimpleTestCase
from domain.exceptions.validation import MissingRequiredFieldException
from domain.value_objects.common import SocialLink
from presentation.request_converters.project.common import request_to_social_link


@dataclass
class ValidSocialLinkData:
    social_links = {"twitter": "https://twitter.com/test", "linkedin": "https://linkedin.com/test"}

    social_links_field = "social_links"

    def to_dict(self):
        return {
            self.social_links_field: self.social_links,
        }


class TestRequestToSocialLink(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidSocialLinkData()

    def test_valid_data(self):
        request = Mock()
        request.data = self.valid_dataclass.to_dict()

        expected = [SocialLink(platform=k, link=v) for k, v in self.valid_dataclass.social_links.items()]

        result = request_to_social_link(request)
        self.assertEqual(expected, result)

    def test_missing_social_links_field(self):
        request = Mock()
        request.data = {}

        with self.assertRaises(MissingRequiredFieldException):
            request_to_social_link(request)
