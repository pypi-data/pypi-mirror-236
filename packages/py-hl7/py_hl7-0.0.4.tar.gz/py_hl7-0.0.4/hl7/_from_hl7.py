import json
import os
from io import BytesIO
from typing import Iterator, Tuple

import openpyxl

from ._config import (
    BASE_PATH,
    CURRENT_HL7_VERSION,
    ENCODING_CHARACTERS,
    FIELD_SEPARATOR,
)

_FIELD_SEPARATOR_FIELD = "<FIELD_SEPARATOR_FIELD>"
_ENCODING_CHARS_FIELD = "<ENCODING_CHARS_FIELD>"
_ENCODING_CHARACTERS_STR = "".join(ENCODING_CHARACTERS)

with open(
    os.path.join(BASE_PATH, "data", f"hl7v{CURRENT_HL7_VERSION}.json"), "r"
) as hl7_meta_data_file:
    HL7_META_DATA = json.loads(hl7_meta_data_file.read())


def hl7_to_csv(hl7_content: str) -> str:
    if f"MSH|{_ENCODING_CHARACTERS_STR}" not in hl7_content:
        raise ValueError("Not a valid HL7 message")

    return _prepare_csv_content(
        "\n".join(
            map(
                lambda csv_line: ";".join(csv_line),
                _convert(
                    hl7_content=_prepare_hl7_content(hl7_content=hl7_content)
                ),
            )
        )
    )


def hl7_to_excel(hl7_content):
    if f"MSH|{_ENCODING_CHARACTERS_STR}" not in hl7_content:
        raise ValueError("Not a valid HL7 message")

    output = BytesIO()
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    for segment, index, value, description in _convert(
        hl7_content=_prepare_hl7_content(hl7_content=hl7_content)
    ):
        if segment == "MSH" and value in [
            _FIELD_SEPARATOR_FIELD,
            _ENCODING_CHARS_FIELD,
        ]:
            value = _prepare_csv_content(value)
        worksheet.append((segment, index, value, description))

    workbook.save(output)
    output.seek(0)
    return output.read()


def _convert(hl7_content: str) -> Iterator[Tuple[str, str, str, str]]:
    for segment in hl7_content.split("\n"):
        fields1 = segment.split(FIELD_SEPARATOR)
        segment_name = fields1[0]
        for index1, field in enumerate(fields1[1:], start=1):
            if not field:
                continue
            for index2, field2 in enumerate(field.split("^"), start=1):
                if not field2:
                    continue
                description = _get_description(segment_name, index1, index2)
                if "&" in field2:
                    for index3, fields3 in enumerate(
                        field2.split("&"), start=1
                    ):
                        yield segment_name, f"{index1}.{index2}.{index3}", fields3, description
                else:
                    yield segment_name, f"{index1}.{index2}", field2, description


def _prepare_hl7_content(hl7_content: str) -> str:
    return hl7_content.replace(
        f"MSH|{_ENCODING_CHARACTERS_STR}",
        f"MSH|{_FIELD_SEPARATOR_FIELD}|{_ENCODING_CHARS_FIELD}",
    )


def _prepare_csv_content(csv_content: str) -> str:
    return csv_content.replace(
        _ENCODING_CHARS_FIELD, _ENCODING_CHARACTERS_STR
    ).replace(_FIELD_SEPARATOR_FIELD, FIELD_SEPARATOR)


def _get_description(segment_name: str, index1: int, index2) -> str:
    key_json = f"{segment_name}.{index1}.{index2}"
    if key_json in HL7_META_DATA:
        return HL7_META_DATA[key_json]["name"]
    return "Description not found"
