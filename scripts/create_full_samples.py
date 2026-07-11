"""
Create the final 139-case Raw and Improved Full sample CSV files.

Inputs:
    Data/Raw/RAW/*.json
    Data/Improved/IMPROVED/*_improved.json
    Data/Full/All/Raw/full_ground_truth_raw.csv
    Data/Full/All/Improved/full_ground_truth_improved.csv

Outputs:
    Data/Full/All/Raw/full_sample_raw.csv
    Data/Full/All/Improved/full_sample_improved.csv

The ground-truth issue-key order is preserved so Raw, Improved, and Ground
Truth remain aligned deterministically.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Sequence


BASE_DIR = Path(__file__).resolve().parents[1]

EXPECTED_CASES = 139

RAW_JSON_DIR = BASE_DIR / "Data" / "Raw" / "RAW"
IMPROVED_JSON_DIR = BASE_DIR / "Data" / "Improved" / "IMPROVED"

FULL_RAW_DIR = BASE_DIR / "Data" / "Full" / "All" / "Raw"
FULL_IMPROVED_DIR = (
    BASE_DIR / "Data" / "Full" / "All" / "Improved"
)

RAW_GROUND_TRUTH = FULL_RAW_DIR / "full_ground_truth_raw.csv"
IMPROVED_GROUND_TRUTH = (
    FULL_IMPROVED_DIR / "full_ground_truth_improved.csv"
)

RAW_OUTPUT = FULL_RAW_DIR / "full_sample_raw.csv"
IMPROVED_OUTPUT = FULL_IMPROVED_DIR / "full_sample_improved.csv"

RAW_FIELDS = [
    "Issue Key",
    "Summary",
    "Type",
    "Affects Version/s",
    "Labels",
    "Confirmation Status",
    "Category",
    "Resolution",
    "Fix Version/s",
    "Description",
]

IMPROVED_FIELDS = [
    "Issue Key",
    "Summary",
    "Type",
    "Affects Version/s",
    "Labels",
    "Confirmation Status",
    "Category",
    "Resolution",
    "Fix Version/s",
    "Description",
    "Steps to Reproduce",
    "Observed Behavior",
    "Expected Behavior",
    "Environment",
]


def normalize_issue_key(value: str) -> str:
    text = str(value or "").strip()

    for suffix in [" Raw", " Improved", "_raw", "_improved"]:
        if text.endswith(suffix):
            text = text[: -len(suffix)].strip()

    return text


def to_text(value: Any) -> str:
    if value is None:
        return "None"

    if isinstance(value, list):
        items = [
            str(item).strip()
            for item in value
            if str(item).strip()
        ]
        return "; ".join(items) if items else "None"

    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False)

    text = str(value).strip()
    return text if text else "None"


def get_first(
    data: Dict[str, Any],
    keys: Sequence[str],
    default: Any = "",
) -> Any:
    for key in keys:
        if key not in data:
            continue

        value = data[key]

        if value is None:
            continue

        if isinstance(value, str) and not value.strip():
            continue

        if isinstance(value, list) and not value:
            continue

        return value

    return default


def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be an object: {path}")

    return data


def read_ground_truth_keys(path: Path) -> List[str]:
    if not path.exists():
        raise FileNotFoundError(f"Ground-truth file not found: {path}")

    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError(f"Ground-truth header is missing: {path}")

        duplicate_headers = {
            name
            for name in reader.fieldnames
            if reader.fieldnames.count(name) > 1
        }

        if duplicate_headers:
            raise ValueError(
                f"Duplicate headers in {path}: "
                f"{sorted(duplicate_headers)}"
            )

        bug_id_column = next(
            (
                name
                for name in reader.fieldnames
                if str(name).strip().lower() == "bug-id"
            ),
            None,
        )

        if bug_id_column is None:
            raise ValueError(
                f"Required BUG-ID column not found in {path}."
            )

        keys: List[str] = []
        seen = set()

        for row in reader:
            issue_key = normalize_issue_key(row.get(bug_id_column, ""))

            if not issue_key:
                continue

            if not issue_key.startswith("MC-"):
                raise ValueError(
                    f"Invalid Mojira issue key in {path}: {issue_key!r}"
                )

            if issue_key in seen:
                raise ValueError(
                    f"Duplicate issue key in {path}: {issue_key}"
                )

            seen.add(issue_key)
            keys.append(issue_key)

    if len(keys) != EXPECTED_CASES:
        raise ValueError(
            f"Expected {EXPECTED_CASES} issue keys in {path}, "
            f"found {len(keys)}."
        )

    return keys


def build_raw_records(issue_keys: Sequence[str]) -> List[Dict[str, str]]:
    records: List[Dict[str, str]] = []

    for issue_key in issue_keys:
        data = read_json(RAW_JSON_DIR / f"{issue_key}.json")

        records.append(
            {
                "Issue Key": issue_key,
                "Summary": to_text(
                    get_first(data, ["summary", "Summary"], "")
                ),
                "Type": to_text(
                    get_first(
                        data,
                        ["type", "Type", "issue_type"],
                        "Bug",
                    )
                ),
                "Affects Version/s": to_text(
                    get_first(
                        data,
                        [
                            "affected_versions",
                            "Affects Version/s",
                            "affects_versions",
                        ],
                        [],
                    )
                ),
                "Labels": to_text(
                    get_first(data, ["labels", "Labels"], [])
                ),
                "Confirmation Status": to_text(
                    get_first(
                        data,
                        [
                            "confirmation_status",
                            "Confirmation Status",
                        ],
                        "Unconfirmed",
                    )
                ),
                "Category": to_text(
                    get_first(
                        data,
                        ["category", "Category"],
                        "(Unassigned)",
                    )
                ),
                "Resolution": to_text(
                    get_first(
                        data,
                        ["resolution", "Resolution"],
                        "None",
                    )
                ),
                "Fix Version/s": to_text(
                    get_first(
                        data,
                        [
                            "fix_versions",
                            "Fix Version/s",
                            "fixVersions",
                        ],
                        [],
                    )
                ),
                "Description": to_text(
                    get_first(
                        data,
                        ["description", "Description"],
                        "",
                    )
                ),
            }
        )

    return records


def build_improved_records(
    issue_keys: Sequence[str],
) -> List[Dict[str, str]]:
    records: List[Dict[str, str]] = []

    for issue_key in issue_keys:
        data = read_json(
            IMPROVED_JSON_DIR / f"{issue_key}_improved.json"
        )

        records.append(
            {
                "Issue Key": issue_key,
                "Summary": to_text(
                    get_first(data, ["summary", "Summary"], "")
                ),
                "Type": to_text(
                    get_first(
                        data,
                        ["type", "Type", "issue_type"],
                        "Bug",
                    )
                ),
                "Affects Version/s": to_text(
                    get_first(
                        data,
                        [
                            "affected_versions",
                            "Affects Version/s",
                            "affects_versions",
                        ],
                        [],
                    )
                ),
                "Labels": to_text(
                    get_first(data, ["labels", "Labels"], [])
                ),
                "Confirmation Status": to_text(
                    get_first(
                        data,
                        [
                            "confirmation_status",
                            "Confirmation Status",
                        ],
                        "Unconfirmed",
                    )
                ),
                "Category": to_text(
                    get_first(
                        data,
                        ["category", "Category"],
                        "(Unassigned)",
                    )
                ),
                "Resolution": to_text(
                    get_first(
                        data,
                        ["resolution", "Resolution"],
                        "None",
                    )
                ),
                "Fix Version/s": to_text(
                    get_first(
                        data,
                        [
                            "fix_versions",
                            "Fix Version/s",
                            "fixVersions",
                        ],
                        [],
                    )
                ),
                "Description": to_text(
                    get_first(
                        data,
                        ["description", "Description"],
                        "",
                    )
                ),
                "Steps to Reproduce": to_text(
                    get_first(
                        data,
                        [
                            "Steps to Reproduce",
                            "steps_to_reproduce",
                            "stepsToReproduce",
                        ],
                        "",
                    )
                ),
                "Observed Behavior": to_text(
                    get_first(
                        data,
                        [
                            "Observed Behavior",
                            "observed_behavior",
                            "observedBehavior",
                        ],
                        "",
                    )
                ),
                "Expected Behavior": to_text(
                    get_first(
                        data,
                        [
                            "Expected Behavior",
                            "expected_behavior",
                            "expectedBehavior",
                        ],
                        "",
                    )
                ),
                "Environment": to_text(
                    get_first(
                        data,
                        ["Environment", "environment"],
                        "",
                    )
                ),
            }
        )

    return records


def write_csv(
    path: Path,
    fieldnames: Sequence[str],
    rows: Sequence[Dict[str, str]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_file = path.with_suffix(path.suffix + ".tmp")

    with temporary_file.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(fieldnames),
            quoting=csv.QUOTE_ALL,
        )
        writer.writeheader()
        writer.writerows(rows)

    temporary_file.replace(path)


def main() -> None:
    print("Creating final Full sample files...")
    print("-" * 70)

    for required_path in [
        RAW_JSON_DIR,
        IMPROVED_JSON_DIR,
        RAW_GROUND_TRUTH,
        IMPROVED_GROUND_TRUTH,
    ]:
        if not required_path.exists():
            raise FileNotFoundError(
                f"Required path not found: {required_path}"
            )

    raw_keys = read_ground_truth_keys(RAW_GROUND_TRUTH)
    improved_keys = read_ground_truth_keys(
        IMPROVED_GROUND_TRUTH
    )

    if raw_keys != improved_keys:
        raw_set = set(raw_keys)
        improved_set = set(improved_keys)

        raise ValueError(
            "Raw and Improved Full ground truths are not aligned. "
            f"Only Raw: {sorted(raw_set - improved_set)[:10]}; "
            f"Only Improved: "
            f"{sorted(improved_set - raw_set)[:10]}."
        )

    raw_records = build_raw_records(raw_keys)
    improved_records = build_improved_records(improved_keys)

    if len(raw_records) != EXPECTED_CASES:
        raise ValueError(
            f"Raw record count is {len(raw_records)}, "
            f"expected {EXPECTED_CASES}."
        )

    if len(improved_records) != EXPECTED_CASES:
        raise ValueError(
            f"Improved record count is {len(improved_records)}, "
            f"expected {EXPECTED_CASES}."
        )

    write_csv(RAW_OUTPUT, RAW_FIELDS, raw_records)
    write_csv(
        IMPROVED_OUTPUT,
        IMPROVED_FIELDS,
        improved_records,
    )

    print(f"Raw output      : {RAW_OUTPUT}")
    print(f"Improved output : {IMPROVED_OUTPUT}")
    print(f"Raw cases       : {len(raw_records)}")
    print(f"Improved cases  : {len(improved_records)}")
    print("-" * 70)
    print("create_full_samples.py completed successfully.")


if __name__ == "__main__":
    main()
