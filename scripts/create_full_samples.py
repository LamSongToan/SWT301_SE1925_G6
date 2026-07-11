"""
create_full_samples.py

Purpose:
    Create full LLM input sample files for Raw and Improved Mojira bug reports.

Why this file is needed:
    full_ground_truth_raw.csv and full_ground_truth_improved.csv are annotation /
    ground truth files. They must be used by compute_metric.py, not as LLM input.
    This script creates separate full_sample_*.csv files that contain bug report
    content for run_experiment.py.

Input:
    Data/Raw/RAW/
        139 raw bug report JSON files, e.g. MC-300962.json

    Data/Improved/IMPROVED/
        139 improved bug report JSON files, e.g. MC-300962_improved.json

    Results/Full/Raw/full_ground_truth_raw.csv
    Results/Full/Improved/full_ground_truth_improved.csv

Output:
    Data/Raw/full_sample_raw.csv
    Data/Improved/full_sample_improved.csv

Run from project root:
    .\\.venv\\Scripts\\python.exe Scripts\\create_full_samples.py

Important:
    This script overwrites existing full_sample_raw.csv and
    full_sample_improved.csv.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict, List


SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent

RAW_JSON_DIR = BASE_DIR / "Data" / "Raw" / "RAW"
IMPROVED_JSON_DIR = BASE_DIR / "Data" / "Improved" / "IMPROVED"

FULL_RAW_DATA_DIR = BASE_DIR / "Data" / "Full" / "Raw"
FULL_IMPROVED_DATA_DIR = BASE_DIR / "Data" / "Full" / "Improved"

RAW_GROUND_TRUTH = (
    FULL_RAW_DATA_DIR / "full_ground_truth_raw.csv"
)

IMPROVED_GROUND_TRUTH = (
    FULL_IMPROVED_DATA_DIR / "full_ground_truth_improved.csv"
)

RAW_OUTPUT = FULL_RAW_DATA_DIR / "full_sample_raw.csv"
IMPROVED_OUTPUT = FULL_IMPROVED_DATA_DIR / "full_sample_improved.csv"

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


def validate_paths() -> None:
    required_paths = [
        RAW_JSON_DIR,
        IMPROVED_JSON_DIR,
        RAW_GROUND_TRUTH,
        IMPROVED_GROUND_TRUTH,
    ]

    for path in required_paths:
        if not path.exists():
            raise FileNotFoundError(f"Required path not found: {path}")

    if not RAW_JSON_DIR.is_dir():
        raise NotADirectoryError(f"Raw JSON path is not a directory: {RAW_JSON_DIR}")

    if not IMPROVED_JSON_DIR.is_dir():
        raise NotADirectoryError(
            f"Improved JSON path is not a directory: {IMPROVED_JSON_DIR}"
        )

    if RAW_GROUND_TRUTH.stat().st_size == 0:
        raise ValueError(f"Raw ground truth file is empty: {RAW_GROUND_TRUTH}")

    if IMPROVED_GROUND_TRUTH.stat().st_size == 0:
        raise ValueError(
            f"Improved ground truth file is empty: {IMPROVED_GROUND_TRUTH}"
        )


def normalize_issue_key(value: str) -> str:
    if value is None:
        return ""

    return (
        value.strip()
        .replace(" Raw", "")
        .replace(" Improved", "")
        .replace("_raw", "")
        .replace("_improved", "")
        .strip()
    )


def to_str(value: Any) -> str:
    if value is None:
        return "None"

    if isinstance(value, list):
        return "; ".join(str(item).strip() for item in value if str(item).strip()) or "None"

    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False)

    text = str(value).strip()

    return text if text else "None"


def get_first(data: Dict[str, Any], keys: List[str], default: Any = "") -> Any:
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
    keys: List[str] = []
    seen_keys = set()
    duplicate_keys = []

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file)
        header = next(reader, None)

        if not header:
            raise ValueError(f"Ground truth file is empty: {path}")

        for row in reader:
            if not row or not row[0].strip():
                continue

            issue_key = normalize_issue_key(row[0])

            if not issue_key.startswith("MC-"):
                continue

            if issue_key in seen_keys:
                duplicate_keys.append(issue_key)
                continue

            seen_keys.add(issue_key)
            keys.append(issue_key)

    if duplicate_keys:
        preview = ", ".join(sorted(set(duplicate_keys))[:10])
        raise ValueError(
            f"Duplicate issue keys found in ground truth file: {path}. "
            f"Examples: {preview}"
        )

    if not keys:
        raise ValueError(f"No issue keys found in ground truth file: {path}")

    return keys


def write_dict_csv(
    path: Path,
    fieldnames: List[str],
    rows: List[Dict[str, Any]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
            quoting=csv.QUOTE_ALL,
        )
        writer.writeheader()
        writer.writerows(rows)


def build_raw_records(issue_keys: List[str]) -> List[Dict[str, Any]]:
    records = []
    missing_json_files = []

    for key in issue_keys:
        json_path = RAW_JSON_DIR / f"{key}.json"

        if not json_path.exists():
            missing_json_files.append(str(json_path))
            continue

        data = read_json(json_path)

        records.append(
            {
                "Issue Key": key,
                "Summary": get_first(data, ["summary", "Summary"], ""),
                "Type": get_first(data, ["type", "Type", "issue_type"], "Bug"),
                "Affects Version/s": to_str(
                    get_first(
                        data,
                        ["affected_versions", "Affects Version/s", "affects_versions"],
                        [],
                    )
                ),
                "Labels": to_str(get_first(data, ["labels", "Labels"], [])),
                "Confirmation Status": to_str(
                    get_first(
                        data,
                        ["confirmation_status", "Confirmation Status"],
                        "Unconfirmed",
                    )
                ),
                "Category": to_str(
                    get_first(data, ["category", "Category"], "(Unassigned)")
                ),
                "Resolution": to_str(
                    get_first(data, ["resolution", "Resolution"], "None")
                ),
                "Fix Version/s": to_str(
                    get_first(data, ["fix_versions", "Fix Version/s", "fixVersions"], [])
                ),
                "Description": get_first(data, ["description", "Description"], ""),
            }
        )

    if missing_json_files:
        raise FileNotFoundError(
            "Missing Raw JSON files:\n" + "\n".join(missing_json_files)
        )

    return records


def build_improved_records(issue_keys: List[str]) -> List[Dict[str, Any]]:
    """
    Build Improved records without duplicating structured sections inside Description.

    The Improved CSV keeps these fields separate:
        - Description
        - Steps to Reproduce
        - Observed Behavior
        - Expected Behavior
        - Environment

    This avoids sending repeated content to the LLM if later code reads all columns.
    """
    records = []
    missing_json_files = []

    for key in issue_keys:
        json_path = IMPROVED_JSON_DIR / f"{key}_improved.json"

        if not json_path.exists():
            missing_json_files.append(str(json_path))
            continue

        data = read_json(json_path)

        records.append(
            {
                "Issue Key": key,
                "Summary": get_first(data, ["summary", "Summary"], ""),
                "Type": get_first(data, ["type", "Type", "issue_type"], "Bug"),
                "Affects Version/s": to_str(
                    get_first(
                        data,
                        ["affected_versions", "Affects Version/s", "affects_versions"],
                        [],
                    )
                ),
                "Labels": to_str(get_first(data, ["labels", "Labels"], [])),
                "Confirmation Status": to_str(
                    get_first(
                        data,
                        ["confirmation_status", "Confirmation Status"],
                        "Unconfirmed",
                    )
                ),
                "Category": to_str(
                    get_first(data, ["category", "Category"], "(Unassigned)")
                ),
                "Resolution": to_str(
                    get_first(data, ["resolution", "Resolution"], "None")
                ),
                "Fix Version/s": to_str(
                    get_first(data, ["fix_versions", "Fix Version/s", "fixVersions"], [])
                ),
                "Description": get_first(data, ["description", "Description"], ""),
                "Steps to Reproduce": get_first(
                    data,
                    ["Steps to Reproduce", "steps_to_reproduce", "stepsToReproduce"],
                    "",
                ),
                "Observed Behavior": get_first(
                    data,
                    ["Observed Behavior", "observed_behavior", "observedBehavior"],
                    "",
                ),
                "Expected Behavior": get_first(
                    data,
                    ["Expected Behavior", "expected_behavior", "expectedBehavior"],
                    "",
                ),
                "Environment": get_first(data, ["Environment", "environment"], ""),
            }
        )

    if missing_json_files:
        raise FileNotFoundError(
            "Missing Improved JSON files:\n" + "\n".join(missing_json_files)
        )

    return records


def validate_key_consistency(raw_keys: List[str], improved_keys: List[str]) -> None:
    raw_set = set(raw_keys)
    improved_set = set(improved_keys)

    missing_in_improved = sorted(raw_set - improved_set)
    missing_in_raw = sorted(improved_set - raw_set)

    print("Checking full Raw vs Improved issue-key consistency:")
    print("-" * 60)

    if not missing_in_improved and not missing_in_raw:
        print("Raw full keys vs Improved full keys: OK")
        print()
        return

    print("Raw full keys vs Improved full keys: NOT OK")
    print(f"Missing in Improved: {missing_in_improved}")
    print(f"Missing in Raw     : {missing_in_raw}")
    print()

    raise ValueError(
        "Raw and Improved full ground truth files do not contain the same issue keys. "
        "Fix the ground truth files before creating full LLM input samples."
    )


def main() -> None:
    print("Creating full sample files for LLM input...")
    print("=" * 60)

    validate_paths()

    raw_keys = read_ground_truth_keys(RAW_GROUND_TRUTH)
    improved_keys = read_ground_truth_keys(IMPROVED_GROUND_TRUTH)

    print(f"Raw ground truth cases      : {len(raw_keys)}")
    print(f"Improved ground truth cases : {len(improved_keys)}")
    print()

    validate_key_consistency(raw_keys, improved_keys)

    raw_records = build_raw_records(raw_keys)
    improved_records = build_improved_records(improved_keys)

    if len(raw_records) != len(raw_keys):
        raise ValueError(
            f"Raw record count mismatch. Keys: {len(raw_keys)}, records: {len(raw_records)}"
        )

    if len(improved_records) != len(improved_keys):
        raise ValueError(
            "Improved record count mismatch. "
            f"Keys: {len(improved_keys)}, records: {len(improved_records)}"
        )

    write_dict_csv(RAW_OUTPUT, RAW_FIELDS, raw_records)
    write_dict_csv(IMPROVED_OUTPUT, IMPROVED_FIELDS, improved_records)

    print("Created files:")
    print("-" * 60)
    print(f"{RAW_OUTPUT} -> {len(raw_records)} rows")
    print(f"{IMPROVED_OUTPUT} -> {len(improved_records)} rows")
    print("=" * 60)
    print("create_full_samples.py completed successfully.")


if __name__ == "__main__":
    main()
