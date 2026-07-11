from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple


BASE_DIR = Path(__file__).resolve().parents[1]

VALID_LABELS = {"Executable", "Non-Executable"}
KAPPA_THRESHOLD = 0.70

METRIC_PHASES = {
    "pilot",
    "development",
    "pilot_validation",
    "holdout",
}

CONFIG = {
    "raw": {
        "ground_truth_dirs": {
            "pilot": BASE_DIR / "Data" / "Raw",
            "development": (
                BASE_DIR / "Data" / "Full" / "Development" / "Raw"
            ),
            "pilot_validation": BASE_DIR / "Data" / "Raw",
            "holdout": (
                BASE_DIR / "Data" / "Full" / "Holdout" / "Raw"
            ),
        },
        "results_dirs": {
            "pilot": BASE_DIR / "Results" / "Raw",
            "development": (
                BASE_DIR / "Results" / "Full" / "Development" / "Raw"
            ),
            "pilot_validation": (
                BASE_DIR
                / "Results"
                / "Full"
                / "Pilot_Validation"
                / "Raw"
            ),
            "holdout": (
                BASE_DIR / "Results" / "Full" / "Holdout" / "Raw"
            ),
        },
        "ground_truth": {
            "pilot": "pilot_ground_truth_raw.csv",
            "development": "development_ground_truth_raw.csv",
            "pilot_validation": "pilot_ground_truth_raw.csv",
            "holdout": "holdout_ground_truth_raw.csv",
        },
        "prediction": {
            "pilot": "pilot_llm_output_raw.csv",
            "development": "development_llm_output_raw.csv",
            "pilot_validation": "pilot_validation_llm_output_raw.csv",
            "holdout": "holdout_llm_output_raw.csv",
        },
        "summary": {
            "pilot": "summary_raw.csv",
            "development": "summary_development_raw.csv",
            "pilot_validation": "summary_pilot_validation_raw.csv",
            "holdout": "summary_holdout_raw.csv",
        },
        "mismatch": {
            "pilot": "mismatch_analysis_raw.csv",
            "development": "mismatch_analysis_development_raw.csv",
            "pilot_validation": (
                "mismatch_analysis_pilot_validation_raw.csv"
            ),
            "holdout": "mismatch_analysis_holdout_raw.csv",
        },
    },
    "improved": {
        "ground_truth_dirs": {
            "pilot": BASE_DIR / "Data" / "Improved",
            "development": (
                BASE_DIR
                / "Data"
                / "Full"
                / "Development"
                / "Improved"
            ),
            "pilot_validation": BASE_DIR / "Data" / "Improved",
            "holdout": (
                BASE_DIR
                / "Data"
                / "Full"
                / "Holdout"
                / "Improved"
            ),
        },
        "results_dirs": {
            "pilot": BASE_DIR / "Results" / "Improved",
            "development": (
                BASE_DIR
                / "Results"
                / "Full"
                / "Development"
                / "Improved"
            ),
            "pilot_validation": (
                BASE_DIR
                / "Results"
                / "Full"
                / "Pilot_Validation"
                / "Improved"
            ),
            "holdout": (
                BASE_DIR
                / "Results"
                / "Full"
                / "Holdout"
                / "Improved"
            ),
        },
        "ground_truth": {
            "pilot": "pilot_ground_truth_improved.csv",
            "development": "development_ground_truth_improved.csv",
            "pilot_validation": "pilot_ground_truth_improved.csv",
            "holdout": "holdout_ground_truth_improved.csv",
        },
        "prediction": {
            "pilot": "pilot_llm_output_improved.csv",
            "development": "development_llm_output_improved.csv",
            "pilot_validation": (
                "pilot_validation_llm_output_improved.csv"
            ),
            "holdout": "holdout_llm_output_improved.csv",
        },
        "summary": {
            "pilot": "summary_improved.csv",
            "development": "summary_development_improved.csv",
            "pilot_validation": (
                "summary_pilot_validation_improved.csv"
            ),
            "holdout": "summary_holdout_improved.csv",
        },
        "mismatch": {
            "pilot": "mismatch_analysis_improved.csv",
            "development": (
                "mismatch_analysis_development_improved.csv"
            ),
            "pilot_validation": (
                "mismatch_analysis_pilot_validation_improved.csv"
            ),
            "holdout": "mismatch_analysis_holdout_improved.csv",
        },
    },
}


def read_csv_dicts(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Cannot find CSV file: {path}")

    if path.stat().st_size == 0:
        raise ValueError(f"CSV file is empty: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))

    if not rows:
        raise ValueError(f"CSV file has no data rows: {path}")

    return rows


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


def normalize_label(value: str) -> str:
    if value is None:
        return ""

    clean = value.strip().lower().replace("_", "-")

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

    return value.strip()


def find_column(row: Dict[str, str], candidates: List[str]) -> str:
    lower_map = {key.strip().lower(): key for key in row.keys()}

    for candidate in candidates:
        actual_key = lower_map.get(candidate.lower())

        if actual_key is not None:
            return row.get(actual_key, "")

    return ""


def get_value(row: Dict[str, str], key: str) -> str:
    return str(row.get(key, "") or "").strip()


def find_issue_key(row: Dict[str, str]) -> str:
    value = find_column(
        row,
        [
            "issue_key",
            "Issue Key",
            "BUG-ID",
            "bug_id",
            "Bug ID",
            "key",
            "Key",
            "id",
            "ID",
        ],
    )

    if value:
        return normalize_issue_key(value)

    for cell in row.values():
        if cell and cell.strip().startswith("MC-"):
            return normalize_issue_key(cell)

    return ""


def find_label(row: Dict[str, str]) -> str:
    value = find_column(
        row,
        [
            # LLM output from run_experiment.py
            "s2r_label",
            "S2R Label",

            # Ground truth / annotation aliases
            "label",
            "Label",
            "ground_truth",
            "Ground Truth",
            "final_label",
            "Final Label",
            "prediction",
            "Prediction",
            "llm_prediction",
            "LLM Prediction",

            # Extra safety for structured output files
            "steps_to_reproduce.label",
            "steps_to_reproduce_label",
        ],
    )

    return normalize_label(value)


def preview_items(items: List[str], limit: int = 10) -> str:
    shown = items[:limit]
    suffix = "" if len(items) <= limit else f", ... (+{len(items) - limit} more)"

    return ", ".join(shown) + suffix


def build_row_map(rows: List[Dict[str, str]], source_name: str) -> Dict[str, Dict[str, str]]:
    row_map: Dict[str, Dict[str, str]] = {}
    duplicate_keys: List[str] = []
    missing_issue_key_rows = 0

    for row in rows:
        issue_key = find_issue_key(row)

        if not issue_key:
            missing_issue_key_rows += 1
            continue

        if issue_key in row_map:
            duplicate_keys.append(issue_key)
            continue

        row_map[issue_key] = row

    if duplicate_keys:
        raise ValueError(
            f"Duplicate issue keys found in {source_name}: "
            f"{preview_items(sorted(set(duplicate_keys)))}"
        )

    if missing_issue_key_rows:
        raise ValueError(
            f"{source_name} contains {missing_issue_key_rows} row(s) without a valid issue key."
        )

    if not row_map:
        raise ValueError(f"No valid issue-key rows found in {source_name}.")

    return row_map


def cohen_kappa(y_true: List[str], y_pred: List[str]) -> float:
    labels = sorted(set(y_true) | set(y_pred))
    n = len(y_true)

    if n == 0:
        return 0.0

    observed_agreement = (
        sum(1 for truth, pred in zip(y_true, y_pred) if truth == pred) / n
    )

    truth_counts = Counter(y_true)
    pred_counts = Counter(y_pred)

    expected_agreement = sum(
        (truth_counts[label] / n) * (pred_counts[label] / n)
        for label in labels
    )

    if expected_agreement == 1:
        return 1.0 if observed_agreement == 1 else 0.0

    return (observed_agreement - expected_agreement) / (1 - expected_agreement)


def classify_kappa_band(kappa: float) -> str:
    if kappa < 0.70:
        return "Below acceptable threshold (< 0.70)"

    if kappa < 0.80:
        return "Acceptable agreement (0.70 <= Kappa < 0.80)"

    if kappa < 1.00:
        return "Good agreement (0.80 <= Kappa < 1.00)"

    return "Perfect agreement (Kappa = 1.00)"


def interpret_kappa(kappa: float, phase: str) -> str:
    if kappa < KAPPA_THRESHOLD:
        if phase == "development":
            return (
                "Below the predefined threshold. Continue improving the "
                "candidate configuration using Development cases only."
            )

        if phase == "pilot_validation":
            return (
                "Below the predefined threshold. The candidate Full "
                "configuration does not preserve acceptable agreement on "
                "the Pilot cases and must not proceed to Holdout."
            )

        if phase == "holdout":
            return (
                "Final protected Holdout agreement is below the threshold. "
                "Report the result as not meeting the research criterion; "
                "do not tune on Holdout cases."
            )

        return (
            "Pilot agreement is below the predefined threshold. "
            "Revise the calibration guidance before proceeding."
        )

    if kappa < 0.80:
        return (
            "Acceptable agreement. The predefined Cohen Kappa threshold "
            "has been met."
        )

    if kappa < 1.00:
        return (
            "Good agreement. The predefined Cohen Kappa threshold "
            "has been exceeded."
        )

    return (
        "Perfect agreement. The predefined threshold has been met; "
        "interpret together with the dataset size and validation design."
    )


def safe_int(value: str) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def safe_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def unique_values(rows: List[Dict[str, str]], column: str) -> str:
    values = sorted(
        {
            row.get(column, "").strip()
            for row in rows
            if row.get(column, "").strip()
        }
    )

    if not values:
        return ""

    return " | ".join(values)


def summarize_usage(prediction_rows: List[Dict[str, str]]) -> Dict[str, str]:
    total_input_tokens = sum(
        safe_int(row.get("input_tokens", "0")) for row in prediction_rows
    )

    total_cached_input_tokens = sum(
        safe_int(row.get("cached_input_tokens", "0")) for row in prediction_rows
    )

    total_output_tokens = sum(
        safe_int(row.get("output_tokens", "0")) for row in prediction_rows
    )

    total_tokens = sum(
        safe_int(row.get("total_tokens", "0")) for row in prediction_rows
    )

    total_cost_usd = sum(
        safe_float(row.get("cost_usd", "0")) for row in prediction_rows
    )

    valid_json_outputs = sum(
        1
        for row in prediction_rows
        if row.get("status", "").strip() == "valid_json"
    )

    valid_label_predictions = sum(
        1
        for row in prediction_rows
        if find_label(row) in VALID_LABELS
    )

    return {
        "model": unique_values(prediction_rows, "model"),
        "prompt_version": unique_values(prediction_rows, "prompt_version"),
        "valid_json_outputs": str(valid_json_outputs),
        "valid_label_predictions": str(valid_label_predictions),
        "total_input_tokens": str(total_input_tokens),
        "total_cached_input_tokens": str(total_cached_input_tokens),
        "total_output_tokens": str(total_output_tokens),
        "total_tokens": str(total_tokens),
        "total_cost_usd": f"{total_cost_usd:.8f}",
    }


def write_summary(path: Path, rows: List[Tuple[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerow(["Metric", "Value"])
        writer.writerows(rows)


def prediction_details(row: Dict[str, str]) -> Dict[str, str]:
    return {
        "prediction_status": get_value(row, "status"),
        "reason": get_value(row, "reason"),
        "s2r_reproducibility": get_value(row, "s2r_reproducibility"),
        "s2r_validity": get_value(row, "s2r_validity"),
        "s2r_failure_type": get_value(row, "s2r_failure_type"),
        "s2r_reason": get_value(row, "s2r_reason"),
        "expected_behavior_presence": get_value(row, "expected_behavior_presence"),
        "expected_behavior_quality": get_value(row, "expected_behavior_quality"),
        "expected_behavior_reason": get_value(row, "expected_behavior_reason"),
        "observed_behavior_presence": get_value(row, "observed_behavior_presence"),
        "observed_behavior_quality": get_value(row, "observed_behavior_quality"),
        "observed_behavior_reason": get_value(row, "observed_behavior_reason"),
        "overall_reason": get_value(row, "overall_reason"),
        "model": get_value(row, "model"),
        "prompt_version": get_value(row, "prompt_version"),
        "cost_usd": get_value(row, "cost_usd"),
    }


def empty_prediction_details() -> Dict[str, str]:
    return {
        "prediction_status": "",
        "reason": "",
        "s2r_reproducibility": "",
        "s2r_validity": "",
        "s2r_failure_type": "",
        "s2r_reason": "",
        "expected_behavior_presence": "",
        "expected_behavior_quality": "",
        "expected_behavior_reason": "",
        "observed_behavior_presence": "",
        "observed_behavior_quality": "",
        "observed_behavior_reason": "",
        "overall_reason": "",
        "model": "",
        "prompt_version": "",
        "cost_usd": "",
    }


def write_mismatches(path: Path, rows: List[Dict[str, str]]) -> None:
    fieldnames = [
        "issue_key",
        "ground_truth",
        "prediction",
        "status",
        "prediction_status",
        "reason",

        "s2r_reproducibility",
        "s2r_validity",
        "s2r_failure_type",
        "s2r_reason",

        "expected_behavior_presence",
        "expected_behavior_quality",
        "expected_behavior_reason",

        "observed_behavior_presence",
        "observed_behavior_quality",
        "observed_behavior_reason",

        "overall_reason",

        "model",
        "prompt_version",
        "cost_usd",
    ]

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows)


def make_mismatch_row(
    issue_key: str,
    ground_truth: str,
    prediction: str,
    status: str,
    details: Dict[str, str],
) -> Dict[str, str]:
    return {
        "issue_key": issue_key,
        "ground_truth": ground_truth,
        "prediction": prediction,
        "status": status,
        **details,
    }


def validate_metric_inputs(ground_truth_file: Path, prediction_file: Path) -> None:
    if not ground_truth_file.exists():
        raise FileNotFoundError(f"Cannot find ground truth file: {ground_truth_file}")

    if ground_truth_file.stat().st_size == 0:
        raise ValueError(f"Ground truth file is empty: {ground_truth_file}")

    if not prediction_file.exists():
        raise FileNotFoundError(
            f"Cannot find prediction file: {prediction_file}. "
            "Run run_experiment.py first."
        )

    if prediction_file.stat().st_size == 0:
        raise ValueError(f"Prediction file is empty: {prediction_file}")


def compute_metrics(
    version: str,
    phase: str,
    confirm_holdout_final: bool = False,
) -> None:
    if phase not in METRIC_PHASES:
        raise ValueError(f"Unsupported metric phase: {phase}")

    if phase == "holdout" and not confirm_holdout_final:
        raise ValueError(
            "Holdout metrics are protected. Use "
            "--confirm-holdout-final only after the final Holdout "
            "predictions have been generated."
        )

    config = CONFIG[version]

    ground_truth_dir = config["ground_truth_dirs"][phase]
    results_dir = config["results_dirs"][phase]

    ground_truth_file = ground_truth_dir / config["ground_truth"][phase]
    prediction_file = results_dir / config["prediction"][phase]
    summary_file = results_dir / config["summary"][phase]
    mismatch_file = results_dir / config["mismatch"][phase]

    validate_metric_inputs(ground_truth_file, prediction_file)

    ground_truth_rows = read_csv_dicts(ground_truth_file)
    prediction_rows = read_csv_dicts(prediction_file)

    ground_truth_map = build_row_map(
        rows=ground_truth_rows,
        source_name=str(ground_truth_file),
    )
    prediction_map = build_row_map(
        rows=prediction_rows,
        source_name=str(prediction_file),
    )

    ground_truth_keys = set(ground_truth_map.keys())
    prediction_keys = set(prediction_map.keys())

    matched_keys = sorted(ground_truth_keys & prediction_keys)
    missing_prediction_keys = sorted(ground_truth_keys - prediction_keys)
    extra_prediction_keys = sorted(prediction_keys - ground_truth_keys)

    y_true = []
    y_pred = []
    mismatches = []

    for key in matched_keys:
        truth_row = ground_truth_map[key]
        prediction_row = prediction_map[key]

        truth = find_label(truth_row)
        pred = find_label(prediction_row)

        details = prediction_details(prediction_row)

        if truth not in VALID_LABELS or pred not in VALID_LABELS:
            mismatches.append(
                make_mismatch_row(
                    issue_key=key,
                    ground_truth=truth,
                    prediction=pred,
                    status="invalid_label",
                    details=details,
                )
            )
            continue

        y_true.append(truth)
        y_pred.append(pred)

        if truth != pred:
            mismatches.append(
                make_mismatch_row(
                    issue_key=key,
                    ground_truth=truth,
                    prediction=pred,
                    status="mismatch",
                    details=details,
                )
            )

    for key in missing_prediction_keys:
        truth = find_label(ground_truth_map[key])

        mismatches.append(
            make_mismatch_row(
                issue_key=key,
                ground_truth=truth,
                prediction="",
                status="missing_prediction",
                details=empty_prediction_details(),
            )
        )

    for key in extra_prediction_keys:
        prediction_row = prediction_map[key]
        pred = find_label(prediction_row)

        mismatches.append(
            make_mismatch_row(
                issue_key=key,
                ground_truth="",
                prediction=pred,
                status="extra_prediction",
                details=prediction_details(prediction_row),
            )
        )

    total_predictions = len(prediction_rows)
    ground_truth_cases = len(ground_truth_map)
    matched_cases = len(matched_keys)
    evaluated_cases = len(y_true)

    correct = sum(1 for truth, pred in zip(y_true, y_pred) if truth == pred)
    incorrect = evaluated_cases - correct

    accuracy = correct / evaluated_cases if evaluated_cases else 0.0
    kappa = cohen_kappa(y_true, y_pred) if evaluated_cases else 0.0
    threshold_passed = kappa >= KAPPA_THRESHOLD
    kappa_band = classify_kappa_band(kappa)
    kappa_interpretation = interpret_kappa(kappa, phase)

    confusion = Counter(zip(y_true, y_pred))

    gt_exec_llm_exec = confusion[("Executable", "Executable")]
    gt_exec_llm_non = confusion[("Executable", "Non-Executable")]
    gt_non_llm_exec = confusion[("Non-Executable", "Executable")]
    gt_non_llm_non = confusion[("Non-Executable", "Non-Executable")]

    usage_summary = summarize_usage(prediction_rows)

    invalid_label_count = sum(1 for row in mismatches if row["status"] == "invalid_label")
    mismatch_count = sum(1 for row in mismatches if row["status"] == "mismatch")

    summary_rows = [
        ("Version", version),
        ("Phase", phase),
        ("Model", usage_summary["model"]),
        ("Prompt version", usage_summary["prompt_version"]),
        ("Prediction file", str(prediction_file)),
        ("Ground truth file", str(ground_truth_file)),
        ("Total prediction rows", str(total_predictions)),
        ("Valid JSON outputs", usage_summary["valid_json_outputs"]),
        ("Valid label predictions", usage_summary["valid_label_predictions"]),
        ("Ground truth cases", str(ground_truth_cases)),
        ("Matched cases", str(matched_cases)),
        ("Evaluated cases", str(evaluated_cases)),
        ("Missing predictions", str(len(missing_prediction_keys))),
        ("Extra predictions", str(len(extra_prediction_keys))),
        ("Invalid labels", str(invalid_label_count)),
        ("Mismatches", str(mismatch_count)),
        ("Correct", str(correct)),
        ("Incorrect", str(incorrect)),
        ("Accuracy", f"{accuracy:.4f}"),
        ("Cohen Kappa", f"{kappa:.4f}"),
        ("Kappa threshold", f"{KAPPA_THRESHOLD:.2f}"),
        ("Threshold passed", str(threshold_passed)),
        ("Kappa band", kappa_band),
        ("Kappa interpretation", kappa_interpretation),
        ("GT Executable -> LLM Executable", str(gt_exec_llm_exec)),
        ("GT Executable -> LLM Non-Executable", str(gt_exec_llm_non)),
        ("GT Non-Executable -> LLM Executable", str(gt_non_llm_exec)),
        ("GT Non-Executable -> LLM Non-Executable", str(gt_non_llm_non)),
        ("Total input tokens", usage_summary["total_input_tokens"]),
        ("Total cached input tokens", usage_summary["total_cached_input_tokens"]),
        ("Total output tokens", usage_summary["total_output_tokens"]),
        ("Total tokens", usage_summary["total_tokens"]),
        ("Total cost USD", usage_summary["total_cost_usd"]),
    ]

    write_summary(summary_file, summary_rows)
    write_mismatches(mismatch_file, mismatches)

    print(f"Computing {version} {phase} metrics...")
    print(f"Prediction file  : {prediction_file}")
    print(f"Ground truth file: {ground_truth_file}")
    print(f"Summary file     : {summary_file}")
    print(f"Mismatch file    : {mismatch_file}")
    print("-" * 60)
    print(f"Model                  : {usage_summary['model']}")
    print(f"Prompt version         : {usage_summary['prompt_version']}")
    print(f"Total prediction rows  : {total_predictions}")
    print(f"Valid JSON outputs     : {usage_summary['valid_json_outputs']}")
    print(f"Valid label predictions: {usage_summary['valid_label_predictions']}")
    print(f"Ground truth cases     : {ground_truth_cases}")
    print(f"Matched cases          : {matched_cases}")
    print(f"Evaluated cases        : {evaluated_cases}")
    print(f"Missing predictions    : {len(missing_prediction_keys)}")
    print(f"Extra predictions      : {len(extra_prediction_keys)}")
    print(f"Invalid labels         : {invalid_label_count}")
    print(f"Mismatches             : {mismatch_count}")
    print(f"Correct                : {correct}")
    print(f"Incorrect              : {incorrect}")
    print(f"Accuracy               : {accuracy:.4f}")
    print(f"Cohen's Kappa          : {kappa:.4f}")
    print(f"Kappa threshold        : {KAPPA_THRESHOLD:.2f}")
    print(f"Threshold passed       : {threshold_passed}")
    print(f"Kappa band             : {kappa_band}")
    print(f"Kappa interpretation   : {kappa_interpretation}")
    print("-" * 60)
    print("Confusion matrix:")
    print(f"Ground Truth Executable     -> LLM Executable    : {gt_exec_llm_exec}")
    print(f"Ground Truth Executable     -> LLM Non-Executable: {gt_exec_llm_non}")
    print(f"Ground Truth Non-Executable -> LLM Executable    : {gt_non_llm_exec}")
    print(f"Ground Truth Non-Executable -> LLM Non-Executable: {gt_non_llm_non}")
    print("-" * 60)
    print(f"Total input tokens        : {usage_summary['total_input_tokens']}")
    print(f"Total cached input tokens : {usage_summary['total_cached_input_tokens']}")
    print(f"Total output tokens       : {usage_summary['total_output_tokens']}")
    print(f"Total tokens              : {usage_summary['total_tokens']}")
    print(f"Total cost USD            : ${usage_summary['total_cost_usd']}")
    print("-" * 60)
    print("compute_metric.py completed successfully.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compute metrics for Raw or Improved LLM predictions."
    )

    parser.add_argument(
        "--version",
        required=True,
        choices=["raw", "improved"],
        help="Dataset version to evaluate.",
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
        help="Experiment phase to evaluate.",
    )

    parser.add_argument(
        "--confirm-holdout-final",
        action="store_true",
        help=(
            "Explicitly confirm final protected Holdout metric "
            "calculation. Required only for --phase holdout."
        ),
    )

    args = parser.parse_args()

    compute_metrics(
        version=args.version,
        phase=args.phase,
        confirm_holdout_final=args.confirm_holdout_final,
    )


if __name__ == "__main__":
    main()
