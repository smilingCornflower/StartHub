import re

from config.settings import MODE

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

PROFILE_PICTURE_PATH = MODE + "/profile_pictures"

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
