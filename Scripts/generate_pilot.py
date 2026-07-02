"""
generate_pilot.py

Purpose:
    Generate pilot dataset files for Raw and Improved Mojira bug reports.

Input:
    Data/Raw/RAW/
        139 raw bug report JSON files

    Data/Improved/IMPROVED/
        139 improved bug report JSON files

    Data/Annotations/
        Author 1 Responses.csv
        Author 2 Responses.csv
        Final Results.csv

Output:
    Data/Raw/
        pilot_sample_raw.csv
        pilot_ground_truth_raw.csv
        pilot_annotation_raw_author1.csv
        pilot_annotation_raw_author2.csv

    Data/Improved/
        pilot_sample_improved.csv
        pilot_ground_truth_improved.csv
        pilot_annotation_improved_author1.csv
        pilot_annotation_improved_author2.csv

Run from project root:
    .\\.venv\\Scripts\\python.exe Scripts\\generate_pilot.py

Important:
    This script overwrites existing pilot files.
    Do not run it again after LLM Results have already been generated,
    unless you intentionally want to regenerate the pilot sample.
"""

from __future__ import annotations

import csv
import json
import random
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent

RAW_JSON_DIR = BASE_DIR / "Data" / "Raw" / "RAW"
IMPROVED_JSON_DIR = BASE_DIR / "Data" / "Improved" / "IMPROVED"

ANNOTATION_DIR = BASE_DIR / "Data" / "Annotations"
FINAL_CSV = ANNOTATION_DIR / "Final Results.csv"
AUTHOR1_CSV = ANNOTATION_DIR / "Author 1 Responses.csv"
AUTHOR2_CSV = ANNOTATION_DIR / "Author 2 Responses.csv"

RAW_OUT_DIR = BASE_DIR / "Data" / "Raw"
IMPROVED_OUT_DIR = BASE_DIR / "Data" / "Improved"

RANDOM_SEED = 210
N_SAMPLE = 26

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
        ANNOTATION_DIR,
        FINAL_CSV,
        AUTHOR1_CSV,
        AUTHOR2_CSV,
    ]

    for path in required_paths:
        if not path.exists():
            raise FileNotFoundError(f"Required path not found: {path}")


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


def load_annotation_rows(
    path: Path,
    tag: str,
) -> Tuple[Optional[List[str]], Dict[str, List[str]]]:
    """
    Load annotation rows by issue key.

    Example first cell:
        MC-300962 Raw
        MC-300962 Improved

    Returned key:
        MC-300962
    """
    header = None
    rows: Dict[str, List[str]] = {}
    suffix = " " + tag

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file)
        header = next(reader, None)

        for row in reader:
            if not row:
                continue

            first_cell = row[0].strip()

            if not first_cell:
                continue

            if not first_cell.endswith(suffix):
                continue

            issue_key = first_cell[: -len(suffix)].strip()
            rows[issue_key] = row

    return header, rows


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


def write_annotation_subset(
    output_path: Path,
    source_csv: Path,
    tag: str,
    sampled_keys: List[str],
) -> None:
    header, data = load_annotation_rows(source_csv, tag)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)

        if header:
            writer.writerow(header)

        for key in sampled_keys:
            row = data.get(key)

            if row:
                writer.writerow(row)
            else:
                blank_count = (len(header) - 1) if header else 9
                writer.writerow([f"{key} {tag}"] + [""] * blank_count)


def build_raw_records(sampled_keys: List[str]) -> List[Dict[str, Any]]:
    records = []

    for key in sampled_keys:
        json_path = RAW_JSON_DIR / f"{key}.json"
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

    return records


def build_improved_records(sampled_keys: List[str]) -> List[Dict[str, Any]]:
    records = []

    for key in sampled_keys:
        json_path = IMPROVED_JSON_DIR / f"{key}_improved.json"
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

    return records


def sample_issue_keys() -> List[str]:
    all_keys = sorted(path.stem for path in RAW_JSON_DIR.glob("*.json"))

    if len(all_keys) < N_SAMPLE:
        raise ValueError(
            f"Not enough raw JSON files to sample. "
            f"Found {len(all_keys)}, need {N_SAMPLE}."
        )

    random.seed(RANDOM_SEED)

    return random.sample(all_keys, N_SAMPLE)


def main() -> None:
    validate_paths()

    RAW_OUT_DIR.mkdir(parents=True, exist_ok=True)
    IMPROVED_OUT_DIR.mkdir(parents=True, exist_ok=True)

    sampled_keys = sample_issue_keys()

    print(f"Sampled {len(sampled_keys)} issues with seed={RANDOM_SEED}")
    print("-" * 60)

    raw_records = build_raw_records(sampled_keys)
    raw_sample_file = RAW_OUT_DIR / "pilot_sample_raw.csv"
    write_dict_csv(raw_sample_file, RAW_FIELDS, raw_records)
    print(f"{raw_sample_file} -> OK")

    improved_records = build_improved_records(sampled_keys)
    improved_sample_file = IMPROVED_OUT_DIR / "pilot_sample_improved.csv"
    write_dict_csv(improved_sample_file, IMPROVED_FIELDS, improved_records)
    print(f"{improved_sample_file} -> OK")

    write_annotation_subset(
        output_path=RAW_OUT_DIR / "pilot_ground_truth_raw.csv",
        source_csv=FINAL_CSV,
        tag="Raw",
        sampled_keys=sampled_keys,
    )
    print(f"{RAW_OUT_DIR / 'pilot_ground_truth_raw.csv'} -> OK")

    write_annotation_subset(
        output_path=IMPROVED_OUT_DIR / "pilot_ground_truth_improved.csv",
        source_csv=FINAL_CSV,
        tag="Improved",
        sampled_keys=sampled_keys,
    )
    print(f"{IMPROVED_OUT_DIR / 'pilot_ground_truth_improved.csv'} -> OK")

    write_annotation_subset(
        output_path=RAW_OUT_DIR / "pilot_annotation_raw_author1.csv",
        source_csv=AUTHOR1_CSV,
        tag="Raw",
        sampled_keys=sampled_keys,
    )
    print(f"{RAW_OUT_DIR / 'pilot_annotation_raw_author1.csv'} -> OK")

    write_annotation_subset(
        output_path=RAW_OUT_DIR / "pilot_annotation_raw_author2.csv",
        source_csv=AUTHOR2_CSV,
        tag="Raw",
        sampled_keys=sampled_keys,
    )
    print(f"{RAW_OUT_DIR / 'pilot_annotation_raw_author2.csv'} -> OK")

    write_annotation_subset(
        output_path=IMPROVED_OUT_DIR / "pilot_annotation_improved_author1.csv",
        source_csv=AUTHOR1_CSV,
        tag="Improved",
        sampled_keys=sampled_keys,
    )
    print(f"{IMPROVED_OUT_DIR / 'pilot_annotation_improved_author1.csv'} -> OK")

    write_annotation_subset(
        output_path=IMPROVED_OUT_DIR / "pilot_annotation_improved_author2.csv",
        source_csv=AUTHOR2_CSV,
        tag="Improved",
        sampled_keys=sampled_keys,
    )
    print(f"{IMPROVED_OUT_DIR / 'pilot_annotation_improved_author2.csv'} -> OK")

    print("-" * 60)
    print("generate_pilot.py completed successfully.")


if __name__ == "__main__":
    main()
