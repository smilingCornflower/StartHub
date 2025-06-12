from pathlib import Path

from config.settings import BASE_DIR
from django.test import SimpleTestCase
from domain.exceptions.file import NotPdfFileException
from domain.services.file import PdfService


class TestPdfService(SimpleTestCase):
    def test_success_is_pdf(self) -> None:
        pdf_file: Path = BASE_DIR / "tests/files/The_C_Programming_Language.pdf"
        with open(pdf_file, "rb") as f:
            PdfService().check_is_pdf(f)

    def test_unsuccessfully_is_pdf(self) -> None:
        not_pdf_file: Path = BASE_DIR / "tests/files/articles.jpg"
        with open(not_pdf_file, "rb") as f:
            with self.assertRaises(NotPdfFileException):
                PdfService().check_is_pdf(f)
        self.assertTrue(f":raises {NotPdfFileException.__name__}:" in PdfService.check_is_pdf.__doc__)
