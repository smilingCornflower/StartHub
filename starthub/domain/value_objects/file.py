from io import BytesIO

from domain.services.file import PdfService
from domain.value_objects import BaseVo
from pydantic import field_validator


class PdfFile(BaseVo):
    value: bytes

    @field_validator("value", mode="after")
    @classmethod
    def is_valid_pdf(cls, value: bytes) -> bytes:
        """:raises NotPdfFileException:"""

        PdfService().check_is_pdf(BytesIO(value))
        return value

    def __str__(self) -> str:
        return f"PdfFile {len(self.value)} bytes"

    def __repr__(self) -> str:
        return f"PdfFile(bytes_len={len(self.value)})"
