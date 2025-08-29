from django.test import SimpleTestCase
from domain.value_objects.common import Id


class TestId(SimpleTestCase):
    def test_int_conversion(self):
        id_obj = Id(value=123)

        result = int(id_obj)
        self.assertEqual(result, 123)
