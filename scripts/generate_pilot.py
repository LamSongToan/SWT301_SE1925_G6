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
        evaluation_metrics.yaml

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

Note:
    evaluation_metrics.yaml is validated only to ensure the research rubric file
    exists. This script does not parse it because this file only generates pilot
    CSV datasets, not LLM evaluation prompts or metric calculations.
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
EVALUATION_METRICS_YAML = ANNOTATION_DIR / "evaluation_metrics.yaml"

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
        EVALUATION_METRICS_YAML,
    ]

    for path in required_paths:
        if not path.exists():
            raise FileNotFoundError(f"Required path not found: {path}")

    if EVALUATION_METRICS_YAML.is_file() and EVALUATION_METRICS_YAML.stat().st_size == 0:
        raise ValueError(f"evaluation_metrics.yaml is empty: {EVALUATION_METRICS_YAML}")


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


def raw_issue_keys() -> set[str]:
    return {path.stem for path in RAW_JSON_DIR.glob("*.json")}


def improved_issue_keys() -> set[str]:
    keys = set()

    for path in IMPROVED_JSON_DIR.glob("*_improved.json"):
        key = path.stem

        if key.endswith("_improved"):
            key = key[: -len("_improved")]

        keys.add(key)

    return keys


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

            if issue_key:
                rows[issue_key] = row

    return header, rows


def annotation_issue_keys(path: Path, tag: str) -> set[str]:
    _, rows = load_annotation_rows(path, tag)
    return set(rows.keys())


def eligible_issue_keys() -> List[str]:
    raw_keys = raw_issue_keys()
    improved_keys = improved_issue_keys()

    final_raw_keys = annotation_issue_keys(FINAL_CSV, "Raw")
    final_improved_keys = annotation_issue_keys(FINAL_CSV, "Improved")

    author1_raw_keys = annotation_issue_keys(AUTHOR1_CSV, "Raw")
    author1_improved_keys = annotation_issue_keys(AUTHOR1_CSV, "Improved")

    author2_raw_keys = annotation_issue_keys(AUTHOR2_CSV, "Raw")
    author2_improved_keys = annotation_issue_keys(AUTHOR2_CSV, "Improved")

    eligible = (
        raw_keys
        & improved_keys
        & final_raw_keys
        & final_improved_keys
        & author1_raw_keys
        & author1_improved_keys
        & author2_raw_keys
        & author2_improved_keys
    )

    if len(eligible) < N_SAMPLE:
        raise ValueError(
            "Not enough eligible issue keys to sample.\n"
            f"Need: {N_SAMPLE}\n"
            f"Eligible: {len(eligible)}\n"
            f"Raw JSON files: {len(raw_keys)}\n"
            f"Improved JSON files: {len(improved_keys)}\n"
            f"Final Raw annotations: {len(final_raw_keys)}\n"
            f"Final Improved annotations: {len(final_improved_keys)}\n"
            f"Author 1 Raw annotations: {len(author1_raw_keys)}\n"
            f"Author 1 Improved annotations: {len(author1_improved_keys)}\n"
            f"Author 2 Raw annotations: {len(author2_raw_keys)}\n"
            f"Author 2 Improved annotations: {len(author2_improved_keys)}"
        )

    return sorted(eligible)


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

    if not header:
        raise ValueError(f"Annotation CSV has no header: {source_csv}")

    missing_keys = [key for key in sampled_keys if key not in data]

    if missing_keys:
        preview = ", ".join(missing_keys[:10])
        raise ValueError(
            f"Missing {tag} annotation rows in {source_csv}. "
            f"Missing count: {len(missing_keys)}. "
            f"Examples: {preview}"
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerow(header)

        for key in sampled_keys:
            writer.writerow(data[key])


def build_raw_records(sampled_keys: List[str]) -> List[Dict[str, Any]]:
    records = []

    for key in sampled_keys:
        json_path = RAW_JSON_DIR / f"{key}.json"
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

    return records


def build_improved_records(sampled_keys: List[str]) -> List[Dict[str, Any]]:
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

    for key in sampled_keys:
        json_path = IMPROVED_JSON_DIR / f"{key}_improved.json"
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

    return records


def sample_issue_keys() -> List[str]:
    keys = eligible_issue_keys()

    random.seed(RANDOM_SEED)

    return random.sample(keys, N_SAMPLE)


def main() -> None:
    validate_paths()

    RAW_OUT_DIR.mkdir(parents=True, exist_ok=True)
    IMPROVED_OUT_DIR.mkdir(parents=True, exist_ok=True)

    sampled_keys = sample_issue_keys()

    print(f"Validated evaluation metrics file: {EVALUATION_METRICS_YAML}")
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
