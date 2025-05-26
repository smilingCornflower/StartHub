import re

CHAR_FIELD_MAX_LENGTH = 255
CHAR_FIELD_MEDIUM_LENGTH = 100
CHAR_FIELD_SHORT_LENGTH = 50

# String consists only of letters (uppercase and lowercase), numbers, hyphens, and underscores.
USERNAME_PATTERN = re.compile(r"^[\w_-]+$", flags=re.UNICODE)
USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 25

PASSWORD_MIN_LENGTH = 6
PASSWORD_MAX_LENGTH = 128

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
