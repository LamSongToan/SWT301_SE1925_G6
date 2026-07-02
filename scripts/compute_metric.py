from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple


BASE_DIR = Path(__file__).resolve().parents[1]

VALID_LABELS = {"Executable", "Non-Executable"}
KAPPA_THRESHOLD = 0.70

CONFIG = {
    "raw": {
        "data_dir": BASE_DIR / "Data" / "Raw",
        "results_dir": BASE_DIR / "Results" / "Raw",
        "ground_truth": {
            "pilot": "pilot_ground_truth_raw.csv",
            "full": "full_ground_truth_raw.csv",
        },
        "prediction": {
            "pilot": "pilot_llm_output_raw.csv",
            "full": "full_llm_output_raw.csv",
        },
        "summary": {
            "pilot": "summary_raw.csv",
            "full": "summary_full_raw.csv",
        },
        "mismatch": {
            "pilot": "mismatch_analysis_raw.csv",
            "full": "mismatch_analysis_full_raw.csv",
        },
    },
    "improved": {
        "data_dir": BASE_DIR / "Data" / "Improved",
        "results_dir": BASE_DIR / "Results" / "Improved",
        "ground_truth": {
            "pilot": "pilot_ground_truth_improved.csv",
            "full": "full_ground_truth_improved.csv",
        },
        "prediction": {
            "pilot": "pilot_llm_output_improved.csv",
            "full": "full_llm_output_improved.csv",
        },
        "summary": {
            "pilot": "summary_improved.csv",
            "full": "summary_full_improved.csv",
        },
        "mismatch": {
            "pilot": "mismatch_analysis_improved.csv",
            "full": "mismatch_analysis_full_improved.csv",
        },
    },
}


def read_csv_dicts(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


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

    if clean in {"non-executable", "non executable", "nonexec", "non-exec"}:
        return "Non-Executable"

    return value.strip()


def find_column(row: Dict[str, str], candidates: List[str]) -> str:
    lower_map = {key.strip().lower(): key for key in row.keys()}

    for candidate in candidates:
        actual_key = lower_map.get(candidate.lower())

        if actual_key is not None:
            return row.get(actual_key, "")

    return ""


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
            "s2r_label",
            "S2R Label",
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
        ],
    )

    return normalize_label(value)


def build_row_map(rows: List[Dict[str, str]]) -> Dict[str, Dict[str, str]]:
    row_map = {}

    for row in rows:
        issue_key = find_issue_key(row)

        if issue_key:
            row_map[issue_key] = row

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
        writer = csv.writer(file)
        writer.writerow(["Metric", "Value"])
        writer.writerows(rows)


def write_mismatches(path: Path, rows: List[Dict[str, str]]) -> None:
    fieldnames = [
        "issue_key",
        "ground_truth",
        "prediction",
        "status",
        "prediction_status",
        "reason",
        "model",
        "prompt_version",
        "cost_usd",
    ]

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def compute_metrics(version: str, phase: str) -> None:
    config = CONFIG[version]

    ground_truth_file = config["data_dir"] / config["ground_truth"][phase]
    prediction_file = config["results_dir"] / config["prediction"][phase]
    summary_file = config["results_dir"] / config["summary"][phase]
    mismatch_file = config["results_dir"] / config["mismatch"][phase]

    if not ground_truth_file.exists():
        raise FileNotFoundError(f"Cannot find ground truth file: {ground_truth_file}")

    if not prediction_file.exists():
        raise FileNotFoundError(
            f"Cannot find prediction file: {prediction_file}. "
            "Run run_experiment.py first."
        )

    ground_truth_rows = read_csv_dicts(ground_truth_file)
    prediction_rows = read_csv_dicts(prediction_file)

    ground_truth_map = build_row_map(ground_truth_rows)
    prediction_map = build_row_map(prediction_rows)

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

        prediction_status = prediction_row.get("status", "").strip()
        reason = prediction_row.get("reason", "").strip()
        model = prediction_row.get("model", "").strip()
        prompt_version = prediction_row.get("prompt_version", "").strip()
        cost_usd = prediction_row.get("cost_usd", "").strip()

        if truth not in VALID_LABELS or pred not in VALID_LABELS:
            mismatches.append(
                {
                    "issue_key": key,
                    "ground_truth": truth,
                    "prediction": pred,
                    "status": "invalid_label",
                    "prediction_status": prediction_status,
                    "reason": reason,
                    "model": model,
                    "prompt_version": prompt_version,
                    "cost_usd": cost_usd,
                }
            )
            continue

        y_true.append(truth)
        y_pred.append(pred)

        if truth != pred:
            mismatches.append(
                {
                    "issue_key": key,
                    "ground_truth": truth,
                    "prediction": pred,
                    "status": "mismatch",
                    "prediction_status": prediction_status,
                    "reason": reason,
                    "model": model,
                    "prompt_version": prompt_version,
                    "cost_usd": cost_usd,
                }
            )

    for key in missing_prediction_keys:
        truth = find_label(ground_truth_map[key])

        mismatches.append(
            {
                "issue_key": key,
                "ground_truth": truth,
                "prediction": "",
                "status": "missing_prediction",
                "prediction_status": "",
                "reason": "",
                "model": "",
                "prompt_version": "",
                "cost_usd": "",
            }
        )

    for key in extra_prediction_keys:
        prediction_row = prediction_map[key]
        pred = find_label(prediction_row)

        mismatches.append(
            {
                "issue_key": key,
                "ground_truth": "",
                "prediction": pred,
                "status": "extra_prediction",
                "prediction_status": prediction_row.get("status", "").strip(),
                "reason": prediction_row.get("reason", "").strip(),
                "model": prediction_row.get("model", "").strip(),
                "prompt_version": prediction_row.get("prompt_version", "").strip(),
                "cost_usd": prediction_row.get("cost_usd", "").strip(),
            }
        )

    total_predictions = len(prediction_rows)
    ground_truth_cases = len(ground_truth_rows)
    matched_cases = len(matched_keys)
    evaluated_cases = len(y_true)

    correct = sum(1 for truth, pred in zip(y_true, y_pred) if truth == pred)
    incorrect = evaluated_cases - correct

    accuracy = correct / evaluated_cases if evaluated_cases else 0.0
    kappa = cohen_kappa(y_true, y_pred) if evaluated_cases else 0.0
    threshold_passed = kappa >= KAPPA_THRESHOLD

    confusion = Counter(zip(y_true, y_pred))

    gt_exec_llm_exec = confusion[("Executable", "Executable")]
    gt_exec_llm_non = confusion[("Executable", "Non-Executable")]
    gt_non_llm_exec = confusion[("Non-Executable", "Executable")]
    gt_non_llm_non = confusion[("Non-Executable", "Non-Executable")]

    usage_summary = summarize_usage(prediction_rows)

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
        ("Correct", str(correct)),
        ("Incorrect", str(incorrect)),
        ("Accuracy", f"{accuracy:.4f}"),
        ("Cohen Kappa", f"{kappa:.4f}"),
        ("Kappa threshold", f"{KAPPA_THRESHOLD:.2f}"),
        ("Threshold passed", str(threshold_passed)),
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
    print(f"Correct                : {correct}")
    print(f"Incorrect              : {incorrect}")
    print(f"Accuracy               : {accuracy:.4f}")
    print(f"Cohen's Kappa          : {kappa:.4f}")
    print(f"Kappa threshold        : {KAPPA_THRESHOLD:.2f}")
    print(f"Threshold passed       : {threshold_passed}")
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
        choices=["pilot", "full"],
        help="Experiment phase to evaluate.",
    )

    args = parser.parse_args()

    compute_metrics(
        version=args.version,
        phase=args.phase,
    )


if __name__ == "__main__":
    main()