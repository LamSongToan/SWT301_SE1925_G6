"""
Create the final Raw Full ground-truth CSV.

Input:
    data/annotations/Final Results.csv

Output:
    data/raw/full_ground_truth_raw.csv

The generator:
    - keeps only Raw rows;
    - removes blank/Unnamed source columns;
    - renames duplicate headers deterministically;
    - validates 139 unique Mojira issue keys;
    - validates canonical S2R labels;
    - overwrites only the final output file.
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
from typing import List, Sequence


BASE_DIR = Path(__file__).resolve().parents[2]

SOURCE_FILE = BASE_DIR / "data" / "annotations" / "Final Results.csv"
OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "full_ground_truth_raw.csv"
)

ROW_SUFFIX = ' Raw'
DISPLAY_NAME = 'Raw'
EXPECTED_CASES = 139
VALID_LABELS = {"Executable", "Non-Executable"}


def make_unique_headers(headers: Sequence[str]) -> List[str]:
    seen: Counter[str] = Counter()
    unique: List[str] = []

    for index, raw_name in enumerate(headers, start=1):
        base_name = str(raw_name).strip() or f"Unnamed_{index}"
        seen[base_name] += 1

        if seen[base_name] == 1:
            unique.append(base_name)
        else:
            unique.append(f"{base_name}_{seen[base_name]}")

    return unique


def normalize_label(value: str) -> str:
    clean = str(value).strip().lower().replace("_", "-")

    if clean in {"executable", "exec"}:
        return "Executable"

    if clean in {
        "non-executable",
        "non executable",
        "nonexec",
        "non-exec",
        "not executable",
        "not-executable",
    }:
        return "Non-Executable"

    return str(value).strip()


def main() -> None:
    print(f"Creating {DISPLAY_NAME} Full ground truth...")
    print("-" * 70)

    if not SOURCE_FILE.exists():
        raise FileNotFoundError(f"Source file not found: {SOURCE_FILE}")

    if SOURCE_FILE.stat().st_size == 0:
        raise ValueError(f"Source file is empty: {SOURCE_FILE}")

    with SOURCE_FILE.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        source_rows = list(csv.reader(file))

    if not source_rows:
        raise ValueError(f"Source file contains no rows: {SOURCE_FILE}")

    source_header = source_rows[0]

    useful_indexes = [
        index
        for index, name in enumerate(source_header)
        if str(name).strip()
        and not str(name).strip().lower().startswith("unnamed")
    ]

    filtered_header = [
        str(source_header[index]).strip()
        for index in useful_indexes
    ]
    output_header = make_unique_headers(filtered_header)

    if "BUG-ID" not in output_header:
        raise ValueError(
            f"Required column 'BUG-ID' is missing. Header: {output_header}"
        )

    if "S2R Label" not in output_header:
        raise ValueError(
            f"Required column 'S2R Label' is missing. Header: {output_header}"
        )

    bug_id_index = output_header.index("BUG-ID")
    label_index = output_header.index("S2R Label")

    selected_rows: List[List[str]] = []
    normalized_keys = set()
    duplicates = []
    invalid_labels = []

    for source_row in source_rows[1:]:
        if not source_row or all(not str(cell).strip() for cell in source_row):
            continue

        padded_row = list(source_row) + [""] * (
            len(source_header) - len(source_row)
        )
        filtered_row = [
            str(padded_row[index]).strip()
            for index in useful_indexes
        ]

        bug_id = filtered_row[bug_id_index]

        if not bug_id.endswith(ROW_SUFFIX):
            continue

        issue_key = bug_id[: -len(ROW_SUFFIX)].strip()
        label = normalize_label(filtered_row[label_index])

        if not issue_key.startswith("MC-"):
            raise ValueError(
                f"Invalid Mojira issue key in {DISPLAY_NAME} row: {bug_id!r}"
            )

        if issue_key in normalized_keys:
            duplicates.append(issue_key)
            continue

        if label not in VALID_LABELS:
            invalid_labels.append(f"{issue_key}={label!r}")
            continue

        normalized_keys.add(issue_key)
        filtered_row[label_index] = label
        selected_rows.append(filtered_row)

    if duplicates:
        raise ValueError(
            "Duplicate issue keys found: "
            + ", ".join(sorted(set(duplicates))[:10])
        )

    if invalid_labels:
        raise ValueError(
            "Invalid S2R labels found: "
            + ", ".join(invalid_labels[:10])
        )

    if len(selected_rows) != EXPECTED_CASES:
        raise ValueError(
            f"Expected {EXPECTED_CASES} {DISPLAY_NAME} cases, "
            f"found {len(selected_rows)}."
        )

    if len(normalized_keys) != EXPECTED_CASES:
        raise ValueError(
            f"Expected {EXPECTED_CASES} unique issue keys, "
            f"found {len(normalized_keys)}."
        )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    temporary_file = OUTPUT_FILE.with_suffix(OUTPUT_FILE.suffix + ".tmp")

    with temporary_file.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerow(output_header)
        writer.writerows(selected_rows)

    temporary_file.replace(OUTPUT_FILE)

    print(f"Source file : {SOURCE_FILE}")
    print(f"Output file : {OUTPUT_FILE}")
    print(f"Cases       : {len(selected_rows)}")
    print(f"Columns     : {len(output_header)}")
    print(f"Header      : {output_header}")
    print("-" * 70)
    print(
        f"create_full_ground_truth_{DISPLAY_NAME.lower()}.py "
        "completed successfully."
    )


if __name__ == "__main__":
    main()
