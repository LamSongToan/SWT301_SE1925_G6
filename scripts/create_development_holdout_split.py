"""
Create the final deterministic Full split:

    26 Pilot issue keys      -> excluded
    75 Development cases    -> tuning and mismatch analysis
    38 Holdout cases        -> final protected evaluation

Inputs:
    Data/Full/All/Raw/full_sample_raw.csv
    Data/Full/All/Raw/full_ground_truth_raw.csv
    Data/Full/All/Improved/full_sample_improved.csv
    Data/Full/All/Improved/full_ground_truth_improved.csv
    Data/Raw/pilot_sample_raw.csv
    Data/Improved/pilot_sample_improved.csv

Outputs:
    Data/Full/Development/...
    Data/Full/Holdout/...
    Data/Full/Split/...

The split is stratified by the joint Raw/Improved S2R label pair using seed 210.
Issue-level split manifests do not expose ground-truth labels.
"""

from __future__ import annotations

import argparse
import csv
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Mapping, Sequence, Set, Tuple


BASE_DIR = Path(__file__).resolve().parents[1]

SPLIT_SEED = 210
EXPECTED_FULL = 139
EXPECTED_PILOT = 26
EXPECTED_REMAINING = 113
DEVELOPMENT_COUNT = 75
HOLDOUT_COUNT = 38

VALID_LABELS = {"Executable", "Non-Executable"}

ALL_RAW_DIR = BASE_DIR / "Data" / "Full" / "All" / "Raw"
ALL_IMPROVED_DIR = (
    BASE_DIR / "Data" / "Full" / "All" / "Improved"
)

DEVELOPMENT_RAW_DIR = (
    BASE_DIR / "Data" / "Full" / "Development" / "Raw"
)
DEVELOPMENT_IMPROVED_DIR = (
    BASE_DIR / "Data" / "Full" / "Development" / "Improved"
)

HOLDOUT_RAW_DIR = (
    BASE_DIR / "Data" / "Full" / "Holdout" / "Raw"
)
HOLDOUT_IMPROVED_DIR = (
    BASE_DIR / "Data" / "Full" / "Holdout" / "Improved"
)

SPLIT_DIR = BASE_DIR / "Data" / "Full" / "Split"

RAW_SAMPLE = ALL_RAW_DIR / "full_sample_raw.csv"
RAW_GT = ALL_RAW_DIR / "full_ground_truth_raw.csv"
IMPROVED_SAMPLE = (
    ALL_IMPROVED_DIR / "full_sample_improved.csv"
)
IMPROVED_GT = (
    ALL_IMPROVED_DIR / "full_ground_truth_improved.csv"
)

PILOT_RAW_SAMPLE = BASE_DIR / "Data" / "Raw" / "pilot_sample_raw.csv"
PILOT_IMPROVED_SAMPLE = (
    BASE_DIR / "Data" / "Improved" / "pilot_sample_improved.csv"
)

OUTPUTS = [
    DEVELOPMENT_RAW_DIR / "development_sample_raw.csv",
    DEVELOPMENT_RAW_DIR / "development_ground_truth_raw.csv",
    DEVELOPMENT_IMPROVED_DIR / "development_sample_improved.csv",
    DEVELOPMENT_IMPROVED_DIR / "development_ground_truth_improved.csv",
    HOLDOUT_RAW_DIR / "holdout_sample_raw.csv",
    HOLDOUT_RAW_DIR / "holdout_ground_truth_raw.csv",
    HOLDOUT_IMPROVED_DIR / "holdout_sample_improved.csv",
    HOLDOUT_IMPROVED_DIR / "holdout_ground_truth_improved.csv",
    SPLIT_DIR / "pilot_issue_keys.csv",
    SPLIT_DIR / "development_issue_keys.csv",
    SPLIT_DIR / "holdout_issue_keys.csv",
    SPLIT_DIR / "split_assignment.csv",
    SPLIT_DIR / "split_summary.csv",
]


def normalize_issue_key(value: str) -> str:
    text = str(value or "").strip()

    for suffix in [" Raw", " Improved", "_raw", "_improved"]:
        if text.endswith(suffix):
            text = text[: -len(suffix)].strip()

    return text


def normalize_label(value: str) -> str:
    clean = str(value or "").strip().lower().replace("_", "-")

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

    return str(value or "").strip()


def read_csv(
    path: Path,
) -> Tuple[List[str], List[Dict[str, str]]]:
    if not path.exists():
        raise FileNotFoundError(f"Required CSV not found: {path}")

    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError(f"CSV header is missing: {path}")

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

        rows = list(reader)

    return list(reader.fieldnames), rows


def find_column(
    fieldnames: Sequence[str],
    candidates: Sequence[str],
) -> str:
    lookup = {
        str(name).strip().lower(): name
        for name in fieldnames
    }

    for candidate in candidates:
        match = lookup.get(candidate.strip().lower())

        if match is not None:
            return match

    raise ValueError(
        f"Cannot find any of {list(candidates)} "
        f"in columns {list(fieldnames)}."
    )


def map_rows(
    fieldnames: Sequence[str],
    rows: Sequence[Dict[str, str]],
    source_name: str,
) -> Tuple[Dict[str, Dict[str, str]], List[str]]:
    key_column = find_column(
        fieldnames,
        ["Issue Key", "BUG-ID", "issue_key", "bug_id"],
    )

    row_map: Dict[str, Dict[str, str]] = {}
    order: List[str] = []

    for row in rows:
        issue_key = normalize_issue_key(row.get(key_column, ""))

        if not issue_key:
            continue

        if not issue_key.startswith("MC-"):
            raise ValueError(
                f"Invalid issue key in {source_name}: {issue_key!r}"
            )

        if issue_key in row_map:
            raise ValueError(
                f"Duplicate issue key in {source_name}: {issue_key}"
            )

        row_map[issue_key] = row
        order.append(issue_key)

    return row_map, order


def label_map(
    fieldnames: Sequence[str],
    rows: Sequence[Dict[str, str]],
    source_name: str,
) -> Dict[str, str]:
    key_column = find_column(
        fieldnames,
        ["BUG-ID", "Issue Key", "issue_key", "bug_id"],
    )
    label_column = find_column(
        fieldnames,
        ["S2R Label", "s2r_label", "label"],
    )

    labels: Dict[str, str] = {}

    for row in rows:
        issue_key = normalize_issue_key(row.get(key_column, ""))

        if not issue_key:
            continue

        label = normalize_label(row.get(label_column, ""))

        if label not in VALID_LABELS:
            raise ValueError(
                f"Invalid label in {source_name}: "
                f"{issue_key}={label!r}"
            )

        if issue_key in labels:
            raise ValueError(
                f"Duplicate label row in {source_name}: {issue_key}"
            )

        labels[issue_key] = label

    return labels


def require_count(
    name: str,
    actual: int,
    expected: int,
) -> None:
    if actual != expected:
        raise ValueError(
            f"{name}: expected {expected}, found {actual}."
        )


def require_same_keys(
    name_a: str,
    keys_a: Set[str],
    name_b: str,
    keys_b: Set[str],
) -> None:
    if keys_a == keys_b:
        return

    raise ValueError(
        f"Issue-key mismatch between {name_a} and {name_b}. "
        f"Only {name_a}: {sorted(keys_a - keys_b)[:10]}; "
        f"Only {name_b}: {sorted(keys_b - keys_a)[:10]}."
    )


def allocate_holdout(
    counts: Mapping[Tuple[str, str], int],
) -> Dict[Tuple[str, str], int]:
    ideal = {
        stratum: count * HOLDOUT_COUNT / EXPECTED_REMAINING
        for stratum, count in counts.items()
    }
    allocation = {
        stratum: math.floor(value)
        for stratum, value in ideal.items()
    }

    remaining = HOLDOUT_COUNT - sum(allocation.values())

    ranked = sorted(
        counts,
        key=lambda stratum: (
            -(ideal[stratum] - math.floor(ideal[stratum])),
            stratum,
        ),
    )

    for stratum in ranked:
        if remaining == 0:
            break

        if allocation[stratum] < counts[stratum]:
            allocation[stratum] += 1
            remaining -= 1

    if remaining != 0:
        raise RuntimeError(
            "Unable to allocate the required Holdout size."
        )

    return allocation


def write_subset(
    path: Path,
    fieldnames: Sequence[str],
    row_map: Mapping[str, Dict[str, str]],
    ordered_keys: Sequence[str],
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

        for issue_key in ordered_keys:
            writer.writerow(row_map[issue_key])

    temporary_file.replace(path)


def write_issue_manifest(
    path: Path,
    split_name: str,
    ordered_keys: Sequence[str],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["issue_key", "split", "split_seed"],
            quoting=csv.QUOTE_ALL,
        )
        writer.writeheader()

        for issue_key in ordered_keys:
            writer.writerow(
                {
                    "issue_key": issue_key,
                    "split": split_name,
                    "split_seed": SPLIT_SEED,
                }
            )


def check_existing(force: bool) -> None:
    existing = [path for path in OUTPUTS if path.exists()]

    if existing and not force:
        raise FileExistsError(
            "The final split already exists. "
            "Use --force only before Holdout evaluation begins."
        )


def main(force: bool) -> None:
    print("Creating final Development/Holdout split...")
    print("-" * 70)

    check_existing(force)

    raw_sample_header, raw_sample_rows = read_csv(RAW_SAMPLE)
    raw_gt_header, raw_gt_rows = read_csv(RAW_GT)
    improved_sample_header, improved_sample_rows = read_csv(
        IMPROVED_SAMPLE
    )
    improved_gt_header, improved_gt_rows = read_csv(
        IMPROVED_GT
    )
    pilot_raw_header, pilot_raw_rows = read_csv(
        PILOT_RAW_SAMPLE
    )
    pilot_improved_header, pilot_improved_rows = read_csv(
        PILOT_IMPROVED_SAMPLE
    )

    raw_sample_map, full_order = map_rows(
        raw_sample_header,
        raw_sample_rows,
        "Raw Full sample",
    )
    raw_gt_map, _ = map_rows(
        raw_gt_header,
        raw_gt_rows,
        "Raw Full ground truth",
    )
    improved_sample_map, _ = map_rows(
        improved_sample_header,
        improved_sample_rows,
        "Improved Full sample",
    )
    improved_gt_map, _ = map_rows(
        improved_gt_header,
        improved_gt_rows,
        "Improved Full ground truth",
    )
    pilot_raw_map, _ = map_rows(
        pilot_raw_header,
        pilot_raw_rows,
        "Raw Pilot sample",
    )
    pilot_improved_map, _ = map_rows(
        pilot_improved_header,
        pilot_improved_rows,
        "Improved Pilot sample",
    )

    raw_labels = label_map(
        raw_gt_header,
        raw_gt_rows,
        "Raw Full ground truth",
    )
    improved_labels = label_map(
        improved_gt_header,
        improved_gt_rows,
        "Improved Full ground truth",
    )

    full_keys = set(raw_sample_map)

    for name, keys in [
        ("Raw Full sample", set(raw_sample_map)),
        ("Raw Full ground truth", set(raw_gt_map)),
        ("Improved Full sample", set(improved_sample_map)),
        ("Improved Full ground truth", set(improved_gt_map)),
        ("Raw Full labels", set(raw_labels)),
        ("Improved Full labels", set(improved_labels)),
    ]:
        require_count(name, len(keys), EXPECTED_FULL)
        require_same_keys(
            "Raw Full sample",
            full_keys,
            name,
            keys,
        )

    pilot_keys = set(pilot_raw_map)

    require_count(
        "Raw Pilot sample",
        len(pilot_raw_map),
        EXPECTED_PILOT,
    )
    require_count(
        "Improved Pilot sample",
        len(pilot_improved_map),
        EXPECTED_PILOT,
    )
    require_same_keys(
        "Raw Pilot sample",
        pilot_keys,
        "Improved Pilot sample",
        set(pilot_improved_map),
    )

    if not pilot_keys <= full_keys:
        raise ValueError(
            "Pilot contains issue keys absent from Full All."
        )

    remaining_keys = full_keys - pilot_keys
    require_count(
        "Remaining non-Pilot cases",
        len(remaining_keys),
        EXPECTED_REMAINING,
    )

    strata: Dict[Tuple[str, str], List[str]] = defaultdict(list)

    for issue_key in sorted(remaining_keys):
        strata[
            (
                raw_labels[issue_key],
                improved_labels[issue_key],
            )
        ].append(issue_key)

    stratum_counts = {
        stratum: len(keys)
        for stratum, keys in strata.items()
    }
    holdout_allocation = allocate_holdout(stratum_counts)

    rng = random.Random(SPLIT_SEED)
    development_keys: Set[str] = set()
    holdout_keys: Set[str] = set()

    for stratum in sorted(strata):
        keys = sorted(strata[stratum])
        rng.shuffle(keys)
        holdout_size = holdout_allocation[stratum]

        holdout_keys.update(keys[:holdout_size])
        development_keys.update(keys[holdout_size:])

    require_count(
        "Development cases",
        len(development_keys),
        DEVELOPMENT_COUNT,
    )
    require_count(
        "Holdout cases",
        len(holdout_keys),
        HOLDOUT_COUNT,
    )

    if pilot_keys & development_keys:
        raise RuntimeError("Pilot overlaps Development.")

    if pilot_keys & holdout_keys:
        raise RuntimeError("Pilot overlaps Holdout.")

    if development_keys & holdout_keys:
        raise RuntimeError("Development overlaps Holdout.")

    if pilot_keys | development_keys | holdout_keys != full_keys:
        raise RuntimeError(
            "Pilot + Development + Holdout do not cover Full All."
        )

    pilot_order = [
        key for key in full_order if key in pilot_keys
    ]
    development_order = [
        key for key in full_order if key in development_keys
    ]
    holdout_order = [
        key for key in full_order if key in holdout_keys
    ]

    write_subset(
        DEVELOPMENT_RAW_DIR / "development_sample_raw.csv",
        raw_sample_header,
        raw_sample_map,
        development_order,
    )
    write_subset(
        DEVELOPMENT_RAW_DIR / "development_ground_truth_raw.csv",
        raw_gt_header,
        raw_gt_map,
        development_order,
    )
    write_subset(
        DEVELOPMENT_IMPROVED_DIR
        / "development_sample_improved.csv",
        improved_sample_header,
        improved_sample_map,
        development_order,
    )
    write_subset(
        DEVELOPMENT_IMPROVED_DIR
        / "development_ground_truth_improved.csv",
        improved_gt_header,
        improved_gt_map,
        development_order,
    )

    write_subset(
        HOLDOUT_RAW_DIR / "holdout_sample_raw.csv",
        raw_sample_header,
        raw_sample_map,
        holdout_order,
    )
    write_subset(
        HOLDOUT_RAW_DIR / "holdout_ground_truth_raw.csv",
        raw_gt_header,
        raw_gt_map,
        holdout_order,
    )
    write_subset(
        HOLDOUT_IMPROVED_DIR / "holdout_sample_improved.csv",
        improved_sample_header,
        improved_sample_map,
        holdout_order,
    )
    write_subset(
        HOLDOUT_IMPROVED_DIR
        / "holdout_ground_truth_improved.csv",
        improved_gt_header,
        improved_gt_map,
        holdout_order,
    )

    write_issue_manifest(
        SPLIT_DIR / "pilot_issue_keys.csv",
        "pilot",
        pilot_order,
    )
    write_issue_manifest(
        SPLIT_DIR / "development_issue_keys.csv",
        "development",
        development_order,
    )
    write_issue_manifest(
        SPLIT_DIR / "holdout_issue_keys.csv",
        "holdout",
        holdout_order,
    )

    assignment_path = SPLIT_DIR / "split_assignment.csv"
    assignment_path.parent.mkdir(parents=True, exist_ok=True)

    with assignment_path.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["issue_key", "split", "split_seed"],
            quoting=csv.QUOTE_ALL,
        )
        writer.writeheader()

        for split_name, keys in [
            ("pilot", pilot_order),
            ("development", development_order),
            ("holdout", holdout_order),
        ]:
            for issue_key in keys:
                writer.writerow(
                    {
                        "issue_key": issue_key,
                        "split": split_name,
                        "split_seed": SPLIT_SEED,
                    }
                )

    summary_path = SPLIT_DIR / "split_summary.csv"

    with summary_path.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["split", "joint_stratum", "count"],
            quoting=csv.QUOTE_ALL,
        )
        writer.writeheader()

        for split_name, keys in [
            ("pilot", pilot_keys),
            ("development", development_keys),
            ("holdout", holdout_keys),
        ]:
            counts = Counter(
                (
                    raw_labels[key],
                    improved_labels[key],
                )
                for key in keys
            )

            for stratum in sorted(counts):
                writer.writerow(
                    {
                        "split": split_name,
                        "joint_stratum": (
                            f"Raw={stratum[0]}|Improved={stratum[1]}"
                        ),
                        "count": counts[stratum],
                    }
                )

            writer.writerow(
                {
                    "split": split_name,
                    "joint_stratum": "TOTAL",
                    "count": len(keys),
                }
            )

    print(f"Split seed       : {SPLIT_SEED}")
    print(f"Pilot cases      : {len(pilot_order)}")
    print(f"Development cases: {len(development_order)}")
    print(f"Holdout cases    : {len(holdout_order)}")
    print("-" * 70)
    print(
        "create_development_holdout_split.py "
        "completed successfully."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Create the deterministic 75-case Development and "
            "38-case Holdout split."
        )
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help=(
            "Overwrite the current split. Use only before "
            "Holdout evaluation begins."
        ),
    )
    args = parser.parse_args()
    main(force=args.force)
