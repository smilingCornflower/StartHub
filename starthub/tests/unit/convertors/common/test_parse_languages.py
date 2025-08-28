from dataclasses import dataclass
from unittest.mock import Mock

from django.http import QueryDict
from django.test import SimpleTestCase
from domain.enums.language import LangCodeEnum
from presentation.request_converters.common import parse_languages


@dataclass
class LanguageData:
    single_lang = "en"
    multiple_langs = "kk,ru,en"
    mixed_valid_invalid_langs = "en,invalid_lang,ru"
    all_invalid_langs = "invalid1,invalid2"

    lang_field = "lang"


class TestParseLanguages(SimpleTestCase):
    def setUp(self):
        self.data = LanguageData()

    def test_single_valid_language(self):
        request = Mock()
        query_params = QueryDict(mutable=True)
        query_params[self.data.lang_field] = self.data.single_lang
        request.query_params = query_params

        expected = [LangCodeEnum(self.data.single_lang)]

        result = parse_languages(request)
        self.assertEqual(expected, result)

    def test_multiple_valid_languages(self):
        request = Mock()
        query_params = QueryDict(mutable=True)
        query_params[self.data.lang_field] = self.data.multiple_langs
        request.query_params = query_params

        expected = [LangCodeEnum("kk"), LangCodeEnum("ru"), LangCodeEnum("en")]

        result = parse_languages(request)
        self.assertEqual(expected, result)

    def test_mixed_valid_and_invalid_languages(self):
        request = Mock()
        query_params = QueryDict(mutable=True)
        query_params[self.data.lang_field] = self.data.mixed_valid_invalid_langs
        request.query_params = query_params

        expected = [LangCodeEnum("en"), LangCodeEnum("ru")]

        result = parse_languages(request)
        self.assertEqual(expected, result)

    def test_all_invalid_languages(self):
        request = Mock()
        query_params = QueryDict(mutable=True)
        query_params[self.data.lang_field] = self.data.all_invalid_langs
        request.query_params = query_params

        expected = []

        result = parse_languages(request)
        self.assertEqual(expected, result)

    def test_no_lang_parameter(self):
        request = Mock()
        query_params = QueryDict()
        request.query_params = query_params

        expected = [LangCodeEnum.get_default()]

        result = parse_languages(request)
        self.assertEqual(expected, result)
