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

    Data/Raw/full_ground_truth_raw.csv
    Data/Improved/full_ground_truth_improved.csv

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

RAW_DATA_DIR = BASE_DIR / "Data" / "Raw"
IMPROVED_DATA_DIR = BASE_DIR / "Data" / "Improved"

RAW_GROUND_TRUTH = RAW_DATA_DIR / "full_ground_truth_raw.csv"
IMPROVED_GROUND_TRUTH = IMPROVED_DATA_DIR / "full_ground_truth_improved.csv"

RAW_OUTPUT = RAW_DATA_DIR / "full_sample_raw.csv"
IMPROVED_OUTPUT = IMPROVED_DATA_DIR / "full_sample_improved.csv"

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
        return "; ".join(str(item) for item in value) if value else "None"

    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False)

    text = str(value).strip()

    return text if text else "None"


def read_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def read_ground_truth_keys(path: Path) -> List[str]:
    keys: List[str] = []

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file)
        header = next(reader, None)

        if not header:
            raise ValueError(f"Ground truth file is empty: {path}")

        for row in reader:
            if not row or not row[0].strip():
                continue

            issue_key = normalize_issue_key(row[0])

            if issue_key.startswith("MC-"):
                keys.append(issue_key)

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
                "Summary": data.get("summary", "") or "",
                "Type": "Bug",
                "Affects Version/s": to_str(data.get("affected_versions", [])),
                "Labels": to_str(data.get("labels", [])),
                "Confirmation Status": data.get("confirmation_status", "")
                or "Unconfirmed",
                "Category": data.get("category", "") or "(Unassigned)",
                "Resolution": data.get("resolution", "") or "None",
                "Fix Version/s": to_str(data.get("fix_versions", [])),
                "Description": data.get("description", "") or "",
            }
        )

    if missing_json_files:
        raise FileNotFoundError(
            "Missing Raw JSON files:\n" + "\n".join(missing_json_files)
        )

    return records


def build_improved_records(issue_keys: List[str]) -> List[Dict[str, Any]]:
    records = []
    missing_json_files = []

    for key in issue_keys:
        json_path = IMPROVED_JSON_DIR / f"{key}_improved.json"

        if not json_path.exists():
            missing_json_files.append(str(json_path))
            continue

        data = read_json(json_path)

        affected_versions = data.get("affected_versions", [])

        if isinstance(affected_versions, str):
            affected_versions = [affected_versions]

        description_parts = [data.get("description", "") or ""]

        for section in [
            "Steps to Reproduce",
            "Observed Behavior",
            "Expected Behavior",
            "Environment",
        ]:
            content = (data.get(section, "") or "").strip()

            if content:
                description_parts.append(f"\n[{section}]\n{content}")

        records.append(
            {
                "Issue Key": key,
                "Summary": data.get("summary", "") or "",
                "Type": "Bug",
                "Affects Version/s": to_str(affected_versions),
                "Labels": to_str(data.get("labels", [])),
                "Confirmation Status": "Unconfirmed",
                "Category": "(Unassigned)",
                "Resolution": data.get("resolution", "") or "None",
                "Fix Version/s": "None",
                "Description": "\n".join(description_parts).strip(),
                "Steps to Reproduce": (
                    data.get("Steps to Reproduce", "") or ""
                ).strip(),
                "Observed Behavior": (
                    data.get("Observed Behavior", "") or ""
                ).strip(),
                "Expected Behavior": (
                    data.get("Expected Behavior", "") or ""
                ).strip(),
                "Environment": (data.get("Environment", "") or "").strip(),
            }
        )

    if missing_json_files:
        raise FileNotFoundError(
            "Missing Improved JSON files:\n" + "\n".join(missing_json_files)
        )

    return records


def print_key_check(raw_keys: List[str], improved_keys: List[str]) -> None:
    raw_set = set(raw_keys)
    improved_set = set(improved_keys)

    missing_in_improved = sorted(raw_set - improved_set)
    missing_in_raw = sorted(improved_set - raw_set)

    print("Checking full Raw vs Improved issue-key consistency:")
    print("-" * 60)

    if not missing_in_improved and not missing_in_raw:
        print("Raw full keys vs Improved full keys: OK")
    else:
        print("Raw full keys vs Improved full keys: NOT OK")
        print(f"Missing in Improved: {missing_in_improved}")
        print(f"Missing in Raw     : {missing_in_raw}")

    print()


def main() -> None:
    print("Creating full sample files for LLM input...")
    print("=" * 60)

    validate_paths()

    raw_keys = read_ground_truth_keys(RAW_GROUND_TRUTH)
    improved_keys = read_ground_truth_keys(IMPROVED_GROUND_TRUTH)

    print(f"Raw ground truth cases      : {len(raw_keys)}")
    print(f"Improved ground truth cases : {len(improved_keys)}")
    print()

    print_key_check(raw_keys, improved_keys)

    raw_records = build_raw_records(raw_keys)
    improved_records = build_improved_records(improved_keys)

    write_dict_csv(RAW_OUTPUT, RAW_FIELDS, raw_records)
    write_dict_csv(IMPROVED_OUTPUT, IMPROVED_FIELDS, improved_records)

    print("Created files:")
    print("-" * 60)
    print(f"{RAW_OUTPUT} -> {len(raw_records)} rows")
    print(f"{IMPROVED_OUTPUT} -> {len(improved_records)} rows")
    print("=" * 60)
    print("Done.")


if __name__ == "__main__":
    main()
