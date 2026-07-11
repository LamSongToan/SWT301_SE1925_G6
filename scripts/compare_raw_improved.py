from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List


BASE_DIR = Path(__file__).resolve().parents[1]

PHASE_PATHS = {
    "pilot": {
        "raw_summary": BASE_DIR / "Results" / "Raw" / "summary_raw.csv",
        "improved_summary": (
            BASE_DIR / "Results" / "Improved" / "summary_improved.csv"
        ),
        "output": (
            BASE_DIR
            / "Results"
            / "comparison_raw_vs_improved_pilot.csv"
        ),
    },
    "development": {
        "raw_summary": (
            BASE_DIR
            / "Results"
            / "Full"
            / "Development"
            / "Raw"
            / "summary_development_raw.csv"
        ),
        "improved_summary": (
            BASE_DIR
            / "Results"
            / "Full"
            / "Development"
            / "Improved"
            / "summary_development_improved.csv"
        ),
        "output": (
            BASE_DIR
            / "Results"
            / "Full"
            / "Development"
            / "comparison_raw_vs_improved_development.csv"
        ),
    },
    "pilot_validation": {
        "raw_summary": (
            BASE_DIR
            / "Results"
            / "Full"
            / "Pilot_Validation"
            / "Raw"
            / "summary_pilot_validation_raw.csv"
        ),
        "improved_summary": (
            BASE_DIR
            / "Results"
            / "Full"
            / "Pilot_Validation"
            / "Improved"
            / "summary_pilot_validation_improved.csv"
        ),
        "output": (
            BASE_DIR
            / "Results"
            / "Full"
            / "Pilot_Validation"
            / "comparison_raw_vs_improved_pilot_validation.csv"
        ),
    },
    "holdout": {
        "raw_summary": (
            BASE_DIR
            / "Results"
            / "Full"
            / "Holdout"
            / "Raw"
            / "summary_holdout_raw.csv"
        ),
        "improved_summary": (
            BASE_DIR
            / "Results"
            / "Full"
            / "Holdout"
            / "Improved"
            / "summary_holdout_improved.csv"
        ),
        "output": (
            BASE_DIR
            / "Results"
            / "Full"
            / "Holdout"
            / "comparison_raw_vs_improved_holdout.csv"
        ),
    },
}

NUMERIC_METRICS = {
    "Total prediction rows",
    "Valid JSON outputs",
    "Valid label predictions",
    "Ground truth cases",
    "Matched cases",
    "Evaluated cases",
    "Missing predictions",
    "Extra predictions",
    "Invalid labels",
    "Mismatches",
    "Correct",
    "Incorrect",
    "Accuracy",
    "Cohen Kappa",
    "Kappa threshold",
    "GT Executable -> LLM Executable",
    "GT Executable -> LLM Non-Executable",
    "GT Non-Executable -> LLM Executable",
    "GT Non-Executable -> LLM Non-Executable",
    "Total input tokens",
    "Total cached input tokens",
    "Total output tokens",
    "Total tokens",
    "Total cost USD",
}

COMPARISON_METRICS = [
    "Version",
    "Phase",
    "Model",
    "Prompt version",
    "Total prediction rows",
    "Valid JSON outputs",
    "Valid label predictions",
    "Ground truth cases",
    "Matched cases",
    "Evaluated cases",
    "Missing predictions",
    "Extra predictions",
    "Invalid labels",
    "Mismatches",
    "Correct",
    "Incorrect",
    "Accuracy",
    "Cohen Kappa",
    "Kappa threshold",
    "Threshold passed",
    "GT Executable -> LLM Executable",
    "GT Executable -> LLM Non-Executable",
    "GT Non-Executable -> LLM Executable",
    "GT Non-Executable -> LLM Non-Executable",
    "Total input tokens",
    "Total cached input tokens",
    "Total output tokens",
    "Total tokens",
    "Total cost USD",
]


def read_summary(path: Path) -> Dict[str, str]:
    if not path.exists():
        raise FileNotFoundError(f"Cannot find summary file: {path}")

    if path.stat().st_size == 0:
        raise ValueError(f"Summary file is empty: {path}")

    summary: Dict[str, str] = {}

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        required_columns = {"Metric", "Value"}

        if not reader.fieldnames or not required_columns.issubset(reader.fieldnames):
            raise ValueError(
                f"Invalid summary format in {path}. "
                "Expected columns: Metric, Value"
            )

        for row in reader:
            metric = row.get("Metric", "").strip()
            value = row.get("Value", "").strip()

            if metric:
                summary[metric] = value

    if not summary:
        raise ValueError(f"No metrics found in summary file: {path}")

    return summary


def to_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def format_difference(metric: str, raw_value: str, improved_value: str) -> str:
    if metric not in NUMERIC_METRICS:
        return ""

    difference = to_float(improved_value) - to_float(raw_value)

    if metric in {
        "Accuracy",
        "Cohen Kappa",
        "Kappa threshold",
    }:
        return f"{difference:.4f}"

    if metric == "Total cost USD":
        return f"{difference:.8f}"

    return str(int(difference)) if difference.is_integer() else f"{difference:.4f}"


def build_interpretation(raw: Dict[str, str], improved: Dict[str, str]) -> List[List[str]]:
    raw_accuracy = to_float(raw.get("Accuracy", "0"))
    improved_accuracy = to_float(improved.get("Accuracy", "0"))

    raw_kappa = to_float(raw.get("Cohen Kappa", "0"))
    improved_kappa = to_float(improved.get("Cohen Kappa", "0"))

    raw_cost = to_float(raw.get("Total cost USD", "0"))
    improved_cost = to_float(improved.get("Total cost USD", "0"))

    raw_invalid_labels = to_float(raw.get("Invalid labels", "0"))
    improved_invalid_labels = to_float(improved.get("Invalid labels", "0"))

    raw_mismatches = to_float(raw.get("Mismatches", "0"))
    improved_mismatches = to_float(improved.get("Mismatches", "0"))

    rows = []

    rows.append(
        [
            "Accuracy change",
            f"{improved_accuracy - raw_accuracy:.4f}",
            "Improved accuracy minus Raw accuracy",
        ]
    )

    rows.append(
        [
            "Cohen Kappa change",
            f"{improved_kappa - raw_kappa:.4f}",
            "Improved Cohen Kappa minus Raw Cohen Kappa",
        ]
    )

    rows.append(
        [
            "Mismatch change",
            f"{improved_mismatches - raw_mismatches:.0f}",
            "Improved mismatches minus Raw mismatches",
        ]
    )

    rows.append(
        [
            "Invalid label change",
            f"{improved_invalid_labels - raw_invalid_labels:.0f}",
            "Improved invalid labels minus Raw invalid labels",
        ]
    )

    rows.append(
        [
            "Cost change USD",
            f"{improved_cost - raw_cost:.8f}",
            "Improved cost minus Raw cost",
        ]
    )

    if improved_kappa >= 0.70:
        conclusion = "Improved reached the target Cohen Kappa threshold."
    else:
        conclusion = "Improved did not reach the target Cohen Kappa threshold."

    rows.append(["Conclusion", conclusion, "Threshold: Cohen Kappa >= 0.70"])

    return rows


def validate_required_metrics(summary: Dict[str, str], summary_name: str) -> None:
    required_metrics = [
        "Accuracy",
        "Cohen Kappa",
        "Total cost USD",
    ]

    missing = [metric for metric in required_metrics if metric not in summary]

    if missing:
        raise ValueError(
            f"{summary_name} is missing required metric(s): {', '.join(missing)}"
        )


def compare(phase: str) -> None:
    phase_paths = PHASE_PATHS.get(phase)

    if phase_paths is None:
        raise ValueError(f"Unsupported comparison phase: {phase}")

    raw_summary = phase_paths["raw_summary"]
    improved_summary = phase_paths["improved_summary"]
    output_file = phase_paths["output"]

    raw = read_summary(raw_summary)
    improved = read_summary(improved_summary)

    validate_required_metrics(raw, str(raw_summary))
    validate_required_metrics(improved, str(improved_summary))

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)

        writer.writerow(["Metric", "Raw", "Improved", "Difference Improved - Raw"])

        for metric in COMPARISON_METRICS:
            raw_value = raw.get(metric, "")
            improved_value = improved.get(metric, "")
            difference = format_difference(metric, raw_value, improved_value)

            writer.writerow([metric, raw_value, improved_value, difference])

        writer.writerow([])
        writer.writerow(["Interpretation", "Value", "Note"])

        for row in build_interpretation(raw, improved):
            writer.writerow(row)

    print(f"Comparing Raw and Improved summaries for phase: {phase}")
    print(f"Raw summary      : {raw_summary}")
    print(f"Improved summary : {improved_summary}")
    print(f"Comparison saved : {output_file}")
    print("-" * 60)
    print(f"Raw Accuracy       : {raw.get('Accuracy', '')}")
    print(f"Improved Accuracy  : {improved.get('Accuracy', '')}")
    print(f"Raw Cohen Kappa    : {raw.get('Cohen Kappa', '')}")
    print(f"Improved Kappa     : {improved.get('Cohen Kappa', '')}")
    print(f"Raw mismatches     : {raw.get('Mismatches', '')}")
    print(f"Improved mismatches: {improved.get('Mismatches', '')}")
    print(f"Raw invalid labels : {raw.get('Invalid labels', '')}")
    print(f"Improved invalid   : {improved.get('Invalid labels', '')}")
    print(f"Raw cost USD       : ${raw.get('Total cost USD', '')}")
    print(f"Improved cost USD  : ${improved.get('Total cost USD', '')}")
    print("-" * 60)
    print("compare_raw_improved.py completed successfully.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare Raw and Improved metric summaries."
    )

    parser.add_argument(
        "--phase",
        required=True,
        choices=[
            "pilot",
            "development",
            "pilot_validation",
            "holdout",
        ],
        help="Experiment phase to compare.",
    )

    args = parser.parse_args()

    compare(args.phase)


if __name__ == "__main__":
    main()
