from pathlib import Path

from domain.value_objects.country import CountryCode

KZ_CODE = CountryCode(value="KZ")
TEST_FILES_PATH = Path(__file__).resolve().parent.parent / "files"
