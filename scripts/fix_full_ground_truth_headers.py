"""
Repair duplicate column names in existing Full/All ground-truth CSV files.

Normal workflow:
    The final create_full_ground_truth_*.py generators already create unique
    headers. This utility is retained only to repair older generated files.

Behavior:
    - no backup file is created;
    - clean files are left unchanged;
    - duplicate names are renamed deterministically:
          Reason, Reason, Reason
      ->  Reason, Reason_2, Reason_3
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
from typing import List, Sequence


BASE_DIR = Path(__file__).resolve().parents[1]
EXPECTED_CASES = 139

FILES = [
    (
        BASE_DIR
        / "Data"
        / "Full"
        / "All"
        / "Raw"
        / "full_ground_truth_raw.csv"
    ),
    (
        BASE_DIR
        / "Data"
        / "Full"
        / "All"
        / "Improved"
        / "full_ground_truth_improved.csv"
    ),
]


def find_duplicates(headers: Sequence[str]) -> dict[str, int]:
    counts = Counter(headers)
    return {
        name: count
        for name, count in counts.items()
        if count > 1
    }


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


def repair_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        rows = list(csv.reader(file))

    if not rows:
        raise ValueError(f"File contains no rows: {path}")

    data_row_count = len(rows) - 1

    if data_row_count != EXPECTED_CASES:
        raise ValueError(
            f"Expected {EXPECTED_CASES} data rows in {path}, "
            f"found {data_row_count}."
        )

    old_header = rows[0]
    old_duplicates = find_duplicates(old_header)

    if not old_duplicates:
        print(f"Already clean: {path}")
        return

    new_header = make_unique_headers(old_header)
    rows[0] = new_header

    temporary_file = path.with_suffix(path.suffix + ".tmp")

    with temporary_file.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerows(rows)

    temporary_file.replace(path)

    print(f"Repaired       : {path}")
    print(f"Old duplicates : {old_duplicates}")
    print(f"New duplicates : {find_duplicates(new_header)}")
    print(f"New header     : {new_header}")


def main() -> None:
    print("Checking Full ground-truth headers...")
    print("-" * 70)

    for path in FILES:
        repair_file(path)

    print("-" * 70)
    print(
        "fix_full_ground_truth_headers.py completed successfully."
    )


if __name__ == "__main__":
    main()
