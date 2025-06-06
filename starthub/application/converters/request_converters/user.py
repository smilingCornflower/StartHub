from django.core.files.uploadedfile import UploadedFile
from loguru import logger


def request_files_to_profile_picture_bytes(files_data: dict[str, UploadedFile]) -> bytes:
    image_file: UploadedFile | None = files_data.get("image")
    if image_file is None:
        logger.error("Image file is not provided.")
        raise KeyError("Key 'image' not found in files_data.")
    logger.info("Image file is provided.")

    image_data: bytes = image_file.read()
    logger.debug(f"image type = {type(image_data)}")

    return image_data
