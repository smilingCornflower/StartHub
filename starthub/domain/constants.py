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


JWT_ALGORITHM = "HS256"
ACCESS_DECODE_OPTIONS = {
    "verify_signature": True,
    "require": ["sub", "email", "iat", "exp", "type"],
}
REFRESH_DECODE_OPTIONS = {
    "verify_signature": True,
    "require": ["sub", "iat", "exp", "type"],
}

COUNTRY_CODE_LENGTH = 2
FUNDING_GOAL_MAX_DIGITS = 12
KZ_BIN_LENGTH = 12

PDF_MAX_SIZE_IN_BYTES = 20 * MEGABYTE
IMAGE_MAX_SIZE_IN_BYTES = 5 * MEGABYTE
PROJECT_IMAGES_MAX_AMOUNT = 7

DESCRIPTION_MAX_LENGTH = 2_000
NEWS_CONTENT_MAX_LENGTH = 2_000


class StorageLocations:
    PROFILE_PICTURE_PATH = MODE + "/profile_pictures"  # + /user_id.jpg
    PROJECT_PLAN_PATH = MODE + "/projects/plans"  # + /project_id.pdf
    PROJECT_PHOTO_PATH = MODE + "/projects/photos"  # + /photo_order.jpg
    NEWS_IMAGE_PATH = MODE + "/news/images"  # + /news_id.jpg
