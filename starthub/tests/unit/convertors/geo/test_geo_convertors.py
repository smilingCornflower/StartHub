from dataclasses import dataclass
from unittest.mock import Mock

from django.http import QueryDict
from django.test import SimpleTestCase
from domain.enums.language import LangCodeEnum
from domain.value_objects.geo import CityGetCommand, RegionGetCommand, RegionName
from presentation.request_converters.geo import request_to_city_get_command, request_to_region_get_command


@dataclass
class ValidGeoData:
    languages = "en,kk"
    region = "almaty-region"

    lang_field = "lang"
    region_field = "region"


class TestRequestToRegionGetCommand(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidGeoData()

    def test_with_languages(self):
        request = Mock()
        query_params = QueryDict(mutable=True)
        query_params[self.valid_dataclass.lang_field] = self.valid_dataclass.languages
        request.query_params = query_params

        expected = RegionGetCommand(languages=[LangCodeEnum("en"), LangCodeEnum("kk")])

        result = request_to_region_get_command(request)
        self.assertEqual(expected, result)

    def test_without_languages(self):
        request = Mock()
        query_params = QueryDict()
        request.query_params = query_params

        expected = RegionGetCommand(languages=[LangCodeEnum.get_default()])

        result = request_to_region_get_command(request)
        self.assertEqual(expected, result)


class TestRequestToCityGetCommand(SimpleTestCase):
    def setUp(self):
        self.valid_dataclass = ValidGeoData()

    def test_with_languages_and_region(self):
        request = Mock()
        query_params = QueryDict(mutable=True)
        query_params[self.valid_dataclass.lang_field] = self.valid_dataclass.languages
        query_params[self.valid_dataclass.region_field] = self.valid_dataclass.region
        request.query_params = query_params

        expected = CityGetCommand(
            languages=[LangCodeEnum("en"), LangCodeEnum("kk")],
            region_name=RegionName(value=self.valid_dataclass.region),
        )

        result = request_to_city_get_command(request)
        self.assertEqual(expected, result)

    def test_with_languages_without_region(self):
        request = Mock()
        query_params = QueryDict(mutable=True)
        query_params[self.valid_dataclass.lang_field] = self.valid_dataclass.languages
        request.query_params = query_params

        expected = CityGetCommand(languages=[LangCodeEnum("en"), LangCodeEnum("kk")], region_name=None)

        result = request_to_city_get_command(request)
        self.assertEqual(expected, result)

    def test_without_languages_with_region(self):
        request = Mock()
        query_params = QueryDict(mutable=True)
        query_params[self.valid_dataclass.region_field] = self.valid_dataclass.region
        request.query_params = query_params

        expected = CityGetCommand(
            languages=[LangCodeEnum.get_default()], region_name=RegionName(value=self.valid_dataclass.region)
        )

        result = request_to_city_get_command(request)
        self.assertEqual(expected, result)

    def test_without_languages_and_region(self):
        request = Mock()
        query_params = QueryDict()
        request.query_params = query_params

        expected = CityGetCommand(languages=[LangCodeEnum.get_default()], region_name=None)

        result = request_to_city_get_command(request)
        self.assertEqual(expected, result)
