"""
kappa_pilot.py

Purpose:
    Compute Cohen's Kappa / Inter-Annotator Agreement (IAA)
    for pilot Raw and Improved annotations.

Input:
    Data/Raw/
        pilot_ground_truth_raw.csv
        pilot_annotation_raw_author1.csv
        pilot_annotation_raw_author2.csv

    Data/Improved/
        pilot_ground_truth_improved.csv
        pilot_annotation_improved_author1.csv
        pilot_annotation_improved_author2.csv

Output:
    Data/Raw/
        kappa_scores_raw.csv

    Data/Improved/
        kappa_scores_improved.csv

Run from project root:
    .\\.venv\\Scripts\\python.exe Scripts\\kappa_pilot.py

Important:
    This script overwrites existing kappa_scores_raw.csv
    and kappa_scores_improved.csv.
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional


SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent

CONFIG = {
    "raw": {
        "tag": "Raw",
        "data_dir": BASE_DIR / "Data" / "Raw",
        "ground_truth": "pilot_ground_truth_raw.csv",
        "author1": "pilot_annotation_raw_author1.csv",
        "author2": "pilot_annotation_raw_author2.csv",
        "output": "kappa_scores_raw.csv",
    },
    "improved": {
        "tag": "Improved",
        "data_dir": BASE_DIR / "Data" / "Improved",
        "ground_truth": "pilot_ground_truth_improved.csv",
        "author1": "pilot_annotation_improved_author1.csv",
        "author2": "pilot_annotation_improved_author2.csv",
        "output": "kappa_scores_improved.csv",
    },
}


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


def clean_text(value: str) -> str:
    if value is None:
        return ""

    return value.strip()


def normalize_text(value: str) -> str:
    return clean_text(value).lower()


def is_empty_annotation(row: Dict[str, str]) -> bool:
    return all(not clean_text(value) for value in row.values())


def score_annotation(row: Dict[str, str]) -> Optional[int]:
    """
    Convert annotation fields into a 1-5 quality score.

    Score logic:
        5 = Executable and has sufficient OB + accurate EB
        4 = Executable but not fully sufficient/accurate
        3 = Non-executable but has both observed and expected behavior
        2 = Non-executable but has either observed or expected behavior
        1 = Very poor / wrong information / missing useful behavior info
    """

    if is_empty_annotation(row):
        return None

    s2r = normalize_text(row.get("s2r", ""))
    irr = normalize_text(row.get("irr", ""))
    ob = normalize_text(row.get("ob", ""))
    obl = normalize_text(row.get("obl", ""))
    eb = normalize_text(row.get("eb", ""))
    ebl = normalize_text(row.get("ebl", ""))

    if s2r == "executable":
        if (
            ob == "present"
            and obl == "sufficient"
            and eb == "present"
            and ebl == "accurate"
        ):
            return 5

        return 4

    if irr == "wrong information":
        return 1

    if ob == "present" and eb == "present":
        return 3

    if ob == "present" or eb == "present":
        return 2

    return 1


def load_annotation_rows(path: Path, tag: str) -> Dict[str, Dict[str, str]]:
    """
    Load annotation rows by issue key.

    Expected first column examples:
        MC-300962 Raw
        MC-300962 Improved

    Used columns by index:
        1 = S2R label
        2 = IRR
        4 = Observed Behavior presence
        5 = Observed Behavior level
        7 = Expected Behavior presence
        8 = Expected Behavior level
    """

    if not path.exists():
        raise FileNotFoundError(f"Cannot find annotation file: {path}")

    rows: Dict[str, Dict[str, str]] = {}
    suffix = " " + tag

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file)

        for row in reader:
            if not row:
                continue

            first_cell = clean_text(row[0])

            if not first_cell:
                continue

            if first_cell.lower() in {"bug id", "issue key", "id"}:
                continue

            if first_cell.endswith(suffix):
                issue_key = first_cell[: -len(suffix)].strip()
            else:
                issue_key = normalize_issue_key(first_cell)

            if not issue_key.startswith("MC-"):
                continue

            def get_cell(index: int) -> str:
                return clean_text(row[index]) if index < len(row) else ""

            rows[issue_key] = {
                "s2r": get_cell(1),
                "irr": get_cell(2),
                "ob": get_cell(4),
                "obl": get_cell(5),
                "eb": get_cell(7),
                "ebl": get_cell(8),
            }

    return rows


def read_pilot_keys(path: Path, tag: str) -> List[str]:
    """
    Read pilot issue keys from pilot_ground_truth file.
    """

    if not path.exists():
        raise FileNotFoundError(f"Cannot find ground truth file: {path}")

    keys: List[str] = []
    suffix = " " + tag

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file)

        for row in reader:
            if not row:
                continue

            first_cell = clean_text(row[0])

            if not first_cell:
                continue

            if first_cell.lower() in {"bug id", "issue key", "id"}:
                continue

            if first_cell.endswith(suffix):
                issue_key = first_cell[: -len(suffix)].strip()
            else:
                issue_key = normalize_issue_key(first_cell)

            if issue_key.startswith("MC-"):
                keys.append(issue_key)

    return keys


def cohen_kappa(
    author1_scores: Dict[str, int],
    author2_scores: Dict[str, int],
    keys: List[str],
) -> float:
    """
    Compute Cohen's Kappa for two annotators.
    """

    n = len(keys)

    if n == 0:
        return 0.0

    observed_agreement = (
        sum(
            1
            for key in keys
            if author1_scores.get(key) == author2_scores.get(key)
        )
        / n
    )

    author1_counts = Counter(author1_scores[key] for key in keys)
    author2_counts = Counter(author2_scores[key] for key in keys)

    labels = sorted(set(author1_counts.keys()) | set(author2_counts.keys()))

    expected_agreement = sum(
        (author1_counts[label] / n) * (author2_counts[label] / n)
        for label in labels
    )

    if expected_agreement == 1:
        return 1.0 if observed_agreement == 1 else 0.0

    return round(
        (observed_agreement - expected_agreement) / (1 - expected_agreement),
        4,
    )


def write_kappa_scores(
    output_path: Path,
    rows: List[Dict[str, str]],
    n: int,
    kappa: float,
    agreement_count: int,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8-sig", newline="") as file:
        fieldnames = [
            "issue_key",
            "author1_score",
            "author2_score",
            "agree",
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

        file.write("\n")
        file.write(f"N,{n},,\n")
        file.write(f"Cohen Kappa,{kappa},,\n")
        file.write(f"Agreement,{agreement_count}/{n},,\n")


def process_version(version: str) -> None:
    config = CONFIG[version]

    tag = config["tag"]
    data_dir = config["data_dir"]

    ground_truth_file = data_dir / config["ground_truth"]
    author1_file = data_dir / config["author1"]
    author2_file = data_dir / config["author2"]
    output_file = data_dir / config["output"]

    print(f"Computing pilot kappa for {version}...")
    print(f"Ground truth : {ground_truth_file}")
    print(f"Author 1     : {author1_file}")
    print(f"Author 2     : {author2_file}")
    print(f"Output       : {output_file}")
    print("-" * 60)

    pilot_keys = read_pilot_keys(ground_truth_file, tag)
    author1_rows = load_annotation_rows(author1_file, tag)
    author2_rows = load_annotation_rows(author2_file, tag)

    output_rows: List[Dict[str, str]] = []

    valid_keys: List[str] = []
    author1_scores: Dict[str, int] = {}
    author2_scores: Dict[str, int] = {}

    for key in pilot_keys:
        author1_score = score_annotation(author1_rows.get(key, {}))
        author2_score = score_annotation(author2_rows.get(key, {}))

        if author1_score is not None and author2_score is not None:
            agree = int(author1_score == author2_score)

            valid_keys.append(key)
            author1_scores[key] = author1_score
            author2_scores[key] = author2_score
        else:
            agree = ""

        output_rows.append(
            {
                "issue_key": key,
                "author1_score": "" if author1_score is None else str(author1_score),
                "author2_score": "" if author2_score is None else str(author2_score),
                "agree": str(agree),
            }
        )

    kappa = cohen_kappa(author1_scores, author2_scores, valid_keys)

    agreement_count = sum(
        1
        for key in valid_keys
        if author1_scores.get(key) == author2_scores.get(key)
    )

    write_kappa_scores(
        output_path=output_file,
        rows=output_rows,
        n=len(valid_keys),
        kappa=kappa,
        agreement_count=agreement_count,
    )

    print(f"Pilot cases      : {len(pilot_keys)}")
    print(f"Valid IAA cases  : {len(valid_keys)}")
    print(f"Agreement        : {agreement_count}/{len(valid_keys)}")
    print(f"Cohen Kappa      : {kappa}")
    print(f"Saved            : {output_file}")
    print()


def main() -> None:
    print("Creating pilot kappa score files...")
    print("=" * 60)

    process_version("raw")
    process_version("improved")

    print("=" * 60)
    print("Done.")


if __name__ == "__main__":
    main()