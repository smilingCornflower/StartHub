from django.test import SimpleTestCase
from domain.value_objects.file import FileVo


class TestFileVo(SimpleTestCase):
    def test_str_representation(self):
        file_obj = FileVo(value=b"test content")

        result = str(file_obj)
        self.assertEqual(result, "FileVo 12 bytes")

    def test_repr_representation(self):
        file_obj = FileVo(value=b"test content")

        result = repr(file_obj)
        self.assertEqual(result, "FileVo(bytes_len=12)")
