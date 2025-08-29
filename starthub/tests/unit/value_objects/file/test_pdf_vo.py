from dataclasses import dataclass
from io import BytesIO

from django.test import SimpleTestCase
from domain.exceptions.file import NotPdfFileException, PdfFileTooLargeException
from domain.value_objects.file import PDF_MAX_SIZE_IN_BYTES, PdfFile
from tests.common.constants import TEST_FILES_PATH
from tests.utils import check_raises


@dataclass
class PdfFileTestData:
    _valid_pdf_content = None
    _too_large_pdf_content = None
    _not_pdf_content = None

    @property
    def valid_pdf_content(self):
        if self._valid_pdf_content is None:
            with open(TEST_FILES_PATH / "file.pdf", mode="rb") as f:
                self._valid_pdf_content = f.read()
        return self._valid_pdf_content

    @property
    def too_large_pdf_content(self):
        if self._too_large_pdf_content is None:
            base = self.valid_pdf_content
            extra = b"0" * (PDF_MAX_SIZE_IN_BYTES - len(base) + 1)
            self._too_large_pdf_content = base + extra
        return self._too_large_pdf_content

    @property
    def not_pdf_content(self):
        if self._not_pdf_content is None:
            with open(TEST_FILES_PATH / "img.jpg", mode="rb") as f:
                self._not_pdf_content = f.read()
        return self._not_pdf_content


class TestPdfFile(SimpleTestCase):
    def setUp(self):
        self.data = PdfFileTestData()

    def test_valid_pdf(self):
        pdf_file = PdfFile(value=self.data.valid_pdf_content)

        self.assertEqual(pdf_file.value, self.data.valid_pdf_content)

    def test_pdf_too_large(self):
        exc = PdfFileTooLargeException

        check_raises(PdfFile.validate_pdf, exc)
        with self.assertRaises(exc):
            PdfFile(value=self.data.too_large_pdf_content)

    def test_not_pdf_file(self):
        exc = NotPdfFileException

        check_raises(PdfFile.validate_pdf, exc)
        with self.assertRaises(exc):
            PdfFile(value=self.data.not_pdf_content)

    def test_str_representation(self):
        pdf_file = PdfFile(value=self.data.valid_pdf_content)

        expected_string = f"PdfFile {len(self.data.valid_pdf_content)} bytes"
        result = str(pdf_file)

        self.assertEqual(result, expected_string)

    def test_repr_representation(self):
        pdf_file = PdfFile(value=self.data.valid_pdf_content)

        expected_representation = f"PdfFile(bytes_len={len(self.data.valid_pdf_content)})"
        result = repr(pdf_file)

        self.assertEqual(result, expected_representation)
