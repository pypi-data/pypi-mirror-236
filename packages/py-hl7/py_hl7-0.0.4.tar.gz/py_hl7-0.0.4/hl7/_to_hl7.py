import csv
from io import StringIO
from typing import Dict, List, Tuple

import openpyxl

from hl7._config import INDEX_SEPARATOR


def csv_to_hl7(csv_content: str) -> str:
    return _to_hl7(_convert(csv_content))


def excel_to_hl7(file_path: str) -> str:
    return csv_to_hl7(
        "\n".join(
            ";".join(map(str, row[:3]))
            for row in openpyxl.load_workbook(file_path).active.iter_rows(
                values_only=True, min_row=2
            )
        )
    )


def _to_hl7(hl7_data: Dict[str, List[List[str]]]) -> str:
    message = ""
    for segment_name, segment_data in hl7_data.items():
        segment_value = "|".join(
            [
                "^".join(
                    [
                        "&".join([l3 or "" for l3 in l2 or []])
                        for l2 in l1 or []
                    ]
                )
                for l1 in segment_data
            ]
        )
        message += f"{segment_name}|{segment_value}\n"
    return message.replace("MSH|||", "MSH|")


def _hl7_index_split(index: str) -> Tuple[int, int, int]:
    indexes = index.split(INDEX_SEPARATOR)
    try:
        index_pipes = int(indexes[0]) - 1
    except IndexError:
        raise ValueError("Error")
    try:
        index_roofs = int(indexes[1]) - 1
    except IndexError:
        index_roofs = 0
    try:
        index_ands = int(indexes[2]) - 1
    except IndexError:
        index_ands = 0
    return index_pipes, index_roofs, index_ands


def _convert(content: str) -> Dict[str, List[List[str]]]:
    hl7_data: Dict = {}
    delimiters_to_try = [";", ","]

    for delimiter in delimiters_to_try:
        data = list(csv.reader(StringIO(content), delimiter=delimiter))

        if len(data[0]) >= 3:
            break

    for segment_name, index, value in map(lambda elem: elem[:3], data):
        index_l1, _, _ = _hl7_index_split(index)
        if segment_name in hl7_data:
            hl7_data[segment_name] = hl7_data[segment_name] + (
                [None] * (index_l1 + 1 - len(hl7_data[segment_name]))
            )
        else:
            hl7_data[segment_name] = [None] * (index_l1 + 1)

    for segment_name, index, value in map(lambda elem: elem[:3], data):
        index_l1, index_l2, _ = _hl7_index_split(index)

        l2_list: List | None = hl7_data[segment_name][index_l1]
        if l2_list is not None:
            hl7_data[segment_name][index_l1] = l2_list + (
                [None] * (index_l2 + 1 - len(l2_list))
            )
        else:
            hl7_data[segment_name][index_l1] = [None] * (index_l2 + 1)

    for segment_name, index, value in map(lambda elem: elem[:3], data):
        index_l1, index_l2, index_l3 = _hl7_index_split(index)
        l3_list: List | None = hl7_data[segment_name][index_l1][index_l2]
        if l3_list is not None:
            hl7_data[segment_name][index_l1][index_l2] = l3_list + (
                [None] * (index_l3 + 1 - len(l3_list))
            )
        else:
            hl7_data[segment_name][index_l1][index_l2] = [None] * (
                index_l3 + 1
            )

    for segment_name, index, value in map(lambda elem: elem[:3], data):
        index_l1, index_l2, index_l3 = _hl7_index_split(index)
        hl7_data[segment_name][index_l1][index_l2][index_l3] = value

    return hl7_data
