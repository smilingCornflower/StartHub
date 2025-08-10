import re

from config.settings import MODE

MEGABYTE = 1024 * 1024  # in kilobytes

CHAR_FIELD_MAX_LENGTH = 255
CHAR_FIELD_MEDIUM_LENGTH = 100
CHAR_FIELD_SHORT_LENGTH = 50

# String consists only of letters (uppercase and lowercase), numbers, hyphens, and underscores.
FIRST_NAME_MAX_LENGTH = CHAR_FIELD_SHORT_LENGTH
LAST_NAME_MAX_LENGTH = CHAR_FIELD_SHORT_LENGTH
NAME_PATTERN = re.compile(r"^[\w_-]+$", flags=re.UNICODE)

PASSWORD_MIN_LENGTH = 6
PASSWORD_MAX_LENGTH = 64
# Passwords contains at least one: lowercase letter, uppercase letter and digit
PASSWORD_PATTERN = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$")

ACCESS_TOKEN_LIFETIME = 15 * 60  # 15 minutes
REFRESH_TOKEN_LIFETIME = 15 * 24 * 3600  # 15 days
ANONYMOUS_TOKEN_LIFETIME = 30 * 24 * 3600  # 30 days

JWT_ALGORITHM = "HS256"
ACCESS_DECODE_OPTIONS = {
    "verify_signature": True,
    "require": ["sub", "email", "iat", "exp", "type"],
}
REFRESH_DECODE_OPTIONS = {
    "verify_signature": True,
    "require": ["sub", "iat", "exp", "type"],
}
ANONYMOUS_DECODE_OPTIONS = {
    "verify_signature": True,
    "require": ["sub", "iat", "exp", "type"],
}

COUNTRY_CODE_LENGTH = 2
FUNDING_GOAL_MAX_DIGITS = 12
PROJECT_CROWDFUNDING_AMOUNT_MAX_DIGITS = 12
KZ_BIN_LENGTH = 12

PDF_MAX_SIZE_IN_BYTES = 20 * MEGABYTE
IMAGE_MAX_SIZE_IN_BYTES = 5 * MEGABYTE
PROJECT_IMAGES_MAX_AMOUNT = 7
PROJECT_STEPS_MAX_AMOUNT = 10

DESCRIPTION_MAX_LENGTH = 2_000

# ==== News ====
NEWS_CONTENT_MAX_LENGTH = 7_000
NEWS_IMAGES_MAX_AMOUNT = 10

# ==== Pagination ====
PAGINNATION_MAX_LMIT = 50


# TODO: Move this attributes to domain PathProvider
class StorageLocations:
    PROFILE_PICTURE_PATH = MODE + "/profile_pictures"  # + /user_id.jpg
    PROJECT_PHOTO_PATH = MODE + "/projects/photos"  # + /photo_order.jpg
    NEWS_IMAGE_PATH = MODE + "/news"  # + news_id/image_uuid.jpg
