from django.test import SimpleTestCase
from domain.exceptions.file import NotPdfFileException
from domain.services.file import PdfService
from msgpack.fallback import BytesIO
from tests.common.check_raises import check_raises
from tests.common.constants import TEST_FILES_PATH


class TestPdfService(SimpleTestCase):
    def test_check_is_pdf_with_pdf(self):
        with open(TEST_FILES_PATH / "file.pdf", mode="rb") as pdf:
            file_data = pdf.read()
        PdfService.check_is_pdf(BytesIO(file_data))

    def test_check_is_pdf_with_jpg(self):
        with open(TEST_FILES_PATH / "img.jpg", mode="rb") as img:
            file_data = img.read()
        exc = NotPdfFileException
        with self.assertRaises(exc):
            PdfService.check_is_pdf(BytesIO(file_data))
        check_raises(PdfService.check_is_pdf, exc)
