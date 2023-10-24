import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

CURRENT_HL7_VERSION = "2.5.1"
FIELD_SEPARATOR = "|"
INDEX_SEPARATOR = "."

ENCODING_CHARACTERS = (
    "^",
    "~",
    "\\",
    "&",
)
