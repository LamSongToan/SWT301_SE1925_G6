from pathlib import Path
import json


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "Results"
RESULTS_DIR.mkdir(exist_ok=True)


def make_notebook(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.x",
                "mimetype": "text/x-python",
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "pygments_lexer": "ipython3",
                "nbconvert_exporter": "python",
                "file_extension": ".py"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }


def md(source):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source
    }


def code(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source
    }


setup_common = """from pathlib import Path
import csv
import math

CURRENT_DIR = Path.cwd()

if (CURRENT_DIR / "Data").exists() and (CURRENT_DIR / "Results").exists():
    PROJECT_ROOT = CURRENT_DIR
elif CURRENT_DIR.name.lower() == "results" and (CURRENT_DIR.parent / "Data").exists():
    PROJECT_ROOT = CURRENT_DIR.parent
else:
    PROJECT_ROOT = CURRENT_DIR

KAPPA_THRESHOLD = 0.70

print("Current dir :", CURRENT_DIR)
print("Project root:", PROJECT_ROOT)
"""


helpers = """def read_csv_rows(path):
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def read_csv_raw_rows(path):
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.reader(file))


def count_data_rows(path):
    rows = read_csv_raw_rows(path)
    return max(len(rows) - 1, 0)


def read_summary(path):
    rows = read_csv_raw_rows(path)

    if not rows:
        raise ValueError(f"Empty summary file: {path}")

    if len(rows[0]) == 2 and len(rows) > 1:
        return {
            row[0].strip(): row[1].strip()
            for row in rows
            if len(row) >= 2 and row[0].strip()
        }

    if len(rows) >= 2:
        header = [col.strip() for col in rows[0]]
        values = rows[1]

        return {
            header[i]: values[i].strip()
            for i in range(min(len(header), len(values)))
        }

    raise ValueError(f"Cannot parse summary file: {path}")


def get_value(summary, possible_keys, default=None):
    normalized = {
        str(key).strip().lower(): value
        for key, value in summary.items()
    }

    for key in possible_keys:
        clean_key = key.strip().lower()

        if clean_key in normalized:
            return normalized[clean_key]

    return default


def to_float(value):
    if value is None:
        return None

    try:
        return float(value)
    except ValueError:
        return None


def normalize_issue_key(value):
    if value is None:
        return ""

    return (
        str(value)
        .strip()
        .replace(" Raw", "")
        .replace(" Improved", "")
        .replace("_raw", "")
        .replace("_improved", "")
        .strip()
    )


def normalize_label(value):
    if value is None:
        return ""

    text = str(value).strip().lower().replace("_", "-")

    if text in {"executable", "exec"}:
        return "Executable"

    if text in {
        "non-executable",
        "non executable",
        "nonexec",
        "non-exec",
        "not executable",
        "not-executable",
    }:
        return "Non-Executable"

    return str(value).strip()


def find_column(row, candidates):
    lower_map = {
        column.strip().lower(): column
        for column in row.keys()
    }

    for candidate in candidates:
        clean_candidate = candidate.strip().lower()

        if clean_candidate in lower_map:
            return lower_map[clean_candidate]

    return None


def print_table(rows, columns):
    if not rows:
        print("(empty)")
        return

    widths = {}

    for column in columns:
        widths[column] = max(
            len(str(column)),
            max(len(str(row.get(column, ""))) for row in rows),
        )

    header = " | ".join(str(column).ljust(widths[column]) for column in columns)
    separator = "-+-".join("-" * widths[column] for column in columns)

    print(header)
    print(separator)

    for row in rows:
        print(" | ".join(str(row.get(column, "")).ljust(widths[column]) for column in columns))


def ascii_bar(label, value, max_value=1.0, width=40):
    if value is None:
        print(f"{label}: N/A")
        return

    filled = int((value / max_value) * width) if max_value else 0
    filled = max(0, min(width, filled))
    bar = "#" * filled + "-" * (width - filled)

    print(f"{label:<10} |{bar}| {value:.4f}")


def describe_values(values):
    clean = [value for value in values if value is not None]

    if not clean:
        return {
            "count": 0,
            "min": None,
            "max": None,
            "mean": None,
        }

    return {
        "count": len(clean),
        "min": round(min(clean), 4),
        "max": round(max(clean), 4),
        "mean": round(sum(clean) / len(clean), 4),
    }


def exact_mcnemar_p_value(b, c):
    n = b + c

    if n == 0:
        return 1.0

    k = min(b, c)
    p_value = 2 * sum(math.comb(n, i) * (0.5 ** n) for i in range(0, k + 1))

    return min(p_value, 1.0)
"""


pilot_cells = [
    md("""# Pilot Analysis

Pilot-stage analysis for the Bug Report Quality Assessment with LLM project.

This notebook reads pilot result files and prints:
- summary metrics
- descriptive statistics
- text-based bars
- prediction label distribution
"""),
    md("## 1. Setup"),
    code(setup_common + """
RAW_RESULTS_DIR = PROJECT_ROOT / "Results" / "Raw"
IMPROVED_RESULTS_DIR = PROJECT_ROOT / "Results" / "Improved"

RAW_SUMMARY = RAW_RESULTS_DIR / "summary_raw.csv"
IMPROVED_SUMMARY = IMPROVED_RESULTS_DIR / "summary_improved.csv"

RAW_MISMATCH = RAW_RESULTS_DIR / "mismatch_analysis_raw.csv"
IMPROVED_MISMATCH = IMPROVED_RESULTS_DIR / "mismatch_analysis_improved.csv"

RAW_LLM_OUTPUT = RAW_RESULTS_DIR / "pilot_llm_output_raw.csv"
IMPROVED_LLM_OUTPUT = IMPROVED_RESULTS_DIR / "pilot_llm_output_improved.csv"
"""),
    md("## 2. Helper Functions"),
    code(helpers),
    md("## 3. Load Pilot Results"),
    code("""raw_summary = read_summary(RAW_SUMMARY)
improved_summary = read_summary(IMPROVED_SUMMARY)

raw_mismatch_cases = count_data_rows(RAW_MISMATCH)
improved_mismatch_cases = count_data_rows(IMPROVED_MISMATCH)

pilot_metrics = [
    {
        "version": "Raw",
        "accuracy": to_float(get_value(raw_summary, ["Accuracy", "accuracy"])),
        "cohen_kappa": to_float(get_value(raw_summary, ["Cohen's Kappa", "Cohen Kappa", "cohen_kappa"])),
        "threshold": KAPPA_THRESHOLD,
        "threshold_passed": str(get_value(raw_summary, ["Threshold passed", "threshold_passed"], "")).lower() == "true",
        "mismatch_cases": raw_mismatch_cases,
    },
    {
        "version": "Improved",
        "accuracy": to_float(get_value(improved_summary, ["Accuracy", "accuracy"])),
        "cohen_kappa": to_float(get_value(improved_summary, ["Cohen's Kappa", "Cohen Kappa", "cohen_kappa"])),
        "threshold": KAPPA_THRESHOLD,
        "threshold_passed": str(get_value(improved_summary, ["Threshold passed", "threshold_passed"], "")).lower() == "true",
        "mismatch_cases": improved_mismatch_cases,
    },
]

print_table(
    pilot_metrics,
    ["version", "accuracy", "cohen_kappa", "threshold", "threshold_passed", "mismatch_cases"],
)
"""),
    md("## 4. Descriptive Statistics"),
    code("""stats_rows = [
    {"metric": "accuracy", **describe_values([row["accuracy"] for row in pilot_metrics])},
    {"metric": "cohen_kappa", **describe_values([row["cohen_kappa"] for row in pilot_metrics])},
    {"metric": "mismatch_cases", **describe_values([row["mismatch_cases"] for row in pilot_metrics])},
]

print_table(stats_rows, ["metric", "count", "min", "max", "mean"])
"""),
    md("## 5. Text-based Bars"),
    code("""print("Accuracy")
for row in pilot_metrics:
    ascii_bar(row["version"], row["accuracy"], max_value=1.0)

print()
print("Cohen's Kappa")
for row in pilot_metrics:
    ascii_bar(row["version"], row["cohen_kappa"], max_value=1.0)

print()
print("Mismatch cases")
max_mismatch = max(row["mismatch_cases"] for row in pilot_metrics)

for row in pilot_metrics:
    ascii_bar(row["version"], row["mismatch_cases"], max_value=max_mismatch)
"""),
    md("## 6. Prediction Label Distribution"),
    code("""def label_distribution(path):
    rows = read_csv_rows(path)

    if not rows:
        return {}

    label_col = find_column(rows[0], ["s2r_label", "S2R Label", "prediction", "llm_prediction"])

    if not label_col:
        return {}

    counts = {}

    for row in rows:
        label = normalize_label(row.get(label_col, ""))
        counts[label] = counts.get(label, 0) + 1

    return counts


raw_label_dist = label_distribution(RAW_LLM_OUTPUT)
improved_label_dist = label_distribution(IMPROVED_LLM_OUTPUT)

label_rows = []

for label, count in raw_label_dist.items():
    label_rows.append({"version": "Raw", "label": label, "count": count})

for label, count in improved_label_dist.items():
    label_rows.append({"version": "Improved", "label": label, "count": count})

print_table(label_rows, ["version", "label", "count"])
"""),
    md("""## 7. Test Choice Note

For pilot data, the sample size is small, so descriptive statistics are the safest focus.
For full paired Raw vs Improved correctness comparison, use McNemar exact test.
"""),
]


full_cells = [
    md("""# Full Analysis

Full-stage analysis for the Bug Report Quality Assessment with LLM project.

This notebook reads full result files and prints:
- summary metrics
- text-based bars
- paired correctness table
- McNemar exact p-value
- accuracy difference
- final conclusion per research question
"""),
    md("## 1. Setup"),
    code(setup_common + """
RAW_RESULTS_DIR = PROJECT_ROOT / "Results" / "Raw"
IMPROVED_RESULTS_DIR = PROJECT_ROOT / "Results" / "Improved"

RAW_SUMMARY = RAW_RESULTS_DIR / "summary_full_raw.csv"
IMPROVED_SUMMARY = IMPROVED_RESULTS_DIR / "summary_full_improved.csv"

RAW_MISMATCH = RAW_RESULTS_DIR / "mismatch_analysis_full_raw.csv"
IMPROVED_MISMATCH = IMPROVED_RESULTS_DIR / "mismatch_analysis_full_improved.csv"

RAW_OUTPUT = RAW_RESULTS_DIR / "full_llm_output_raw.csv"
IMPROVED_OUTPUT = IMPROVED_RESULTS_DIR / "full_llm_output_improved.csv"

RAW_GROUND_TRUTH = PROJECT_ROOT / "Data" / "Raw" / "full_ground_truth_raw.csv"
IMPROVED_GROUND_TRUTH = PROJECT_ROOT / "Data" / "Improved" / "full_ground_truth_improved.csv"
"""),
    md("## 2. Helper Functions"),
    code(helpers),
    md("## 3. Load Full Results"),
    code("""raw_summary = read_summary(RAW_SUMMARY)
improved_summary = read_summary(IMPROVED_SUMMARY)

raw_mismatch_cases = count_data_rows(RAW_MISMATCH)
improved_mismatch_cases = count_data_rows(IMPROVED_MISMATCH)

full_metrics = [
    {
        "version": "Raw",
        "accuracy": to_float(get_value(raw_summary, ["Accuracy", "accuracy"])),
        "cohen_kappa": to_float(get_value(raw_summary, ["Cohen's Kappa", "Cohen Kappa", "cohen_kappa"])),
        "threshold": KAPPA_THRESHOLD,
        "threshold_passed": str(get_value(raw_summary, ["Threshold passed", "threshold_passed"], "")).lower() == "true",
        "mismatch_cases": raw_mismatch_cases,
    },
    {
        "version": "Improved",
        "accuracy": to_float(get_value(improved_summary, ["Accuracy", "accuracy"])),
        "cohen_kappa": to_float(get_value(improved_summary, ["Cohen's Kappa", "Cohen Kappa", "cohen_kappa"])),
        "threshold": KAPPA_THRESHOLD,
        "threshold_passed": str(get_value(improved_summary, ["Threshold passed", "threshold_passed"], "")).lower() == "true",
        "mismatch_cases": improved_mismatch_cases,
    },
]

print_table(
    full_metrics,
    ["version", "accuracy", "cohen_kappa", "threshold", "threshold_passed", "mismatch_cases"],
)
"""),
    md("## 4. Text-based Bars"),
    code("""print("Accuracy")
for row in full_metrics:
    ascii_bar(row["version"], row["accuracy"], max_value=1.0)

print()
print("Cohen's Kappa")
for row in full_metrics:
    ascii_bar(row["version"], row["cohen_kappa"], max_value=1.0)

print()
print("Mismatch cases")
max_mismatch = max(row["mismatch_cases"] for row in full_metrics)

for row in full_metrics:
    ascii_bar(row["version"], row["mismatch_cases"], max_value=max_mismatch)
"""),
    md("## 5. Paired Correctness Table"),
    code("""def build_correctness_table(output_path, ground_truth_path, version):
    pred_rows = read_csv_rows(output_path)
    gt_rows = read_csv_rows(ground_truth_path)

    if not pred_rows:
        raise ValueError(f"No prediction rows found for {version}")

    if not gt_rows:
        raise ValueError(f"No ground truth rows found for {version}")

    pred_key_col = find_column(pred_rows[0], ["issue_key", "Issue Key", "BUG-ID", "Bug ID"])
    pred_label_col = find_column(pred_rows[0], ["s2r_label", "S2R Label", "prediction", "llm_prediction"])

    gt_key_col = find_column(gt_rows[0], ["BUG-ID", "issue_key", "Issue Key", "Bug ID"])
    gt_label_col = find_column(gt_rows[0], ["S2R Label", "s2r_label", "label", "ground_truth"])

    if not pred_key_col or not pred_label_col:
        raise ValueError(f"Cannot find prediction key/label columns for {version}")

    if not gt_key_col or not gt_label_col:
        raise ValueError(f"Cannot find ground truth key/label columns for {version}")

    prediction_by_key = {}

    for row in pred_rows:
        issue_key = normalize_issue_key(row.get(pred_key_col, ""))
        label = normalize_label(row.get(pred_label_col, ""))

        if issue_key:
            prediction_by_key[issue_key] = label

    correctness = {}

    for row in gt_rows:
        issue_key = normalize_issue_key(row.get(gt_key_col, ""))
        ground_truth = normalize_label(row.get(gt_label_col, ""))

        if issue_key and issue_key in prediction_by_key:
            correctness[issue_key] = ground_truth == prediction_by_key[issue_key]

    return correctness


raw_correct = build_correctness_table(RAW_OUTPUT, RAW_GROUND_TRUTH, "Raw")
improved_correct = build_correctness_table(IMPROVED_OUTPUT, IMPROVED_GROUND_TRUTH, "Improved")

paired_keys = sorted(set(raw_correct.keys()) & set(improved_correct.keys()))

paired = [
    {
        "issue_key": key,
        "raw_correct": raw_correct[key],
        "improved_correct": improved_correct[key],
    }
    for key in paired_keys
]

print("Paired cases:", len(paired))
print_table(paired[:10], ["issue_key", "raw_correct", "improved_correct"])
"""),
    md("## 6. McNemar Exact Test"),
    code("""both_correct = sum(row["raw_correct"] and row["improved_correct"] for row in paired)
raw_correct_improved_wrong = sum(row["raw_correct"] and not row["improved_correct"] for row in paired)
raw_wrong_improved_correct = sum((not row["raw_correct"]) and row["improved_correct"] for row in paired)
both_wrong = sum((not row["raw_correct"]) and (not row["improved_correct"]) for row in paired)

mcnemar_matrix = [
    {
        "Raw": "Correct",
        "Improved correct": both_correct,
        "Improved wrong": raw_correct_improved_wrong,
    },
    {
        "Raw": "Wrong",
        "Improved correct": raw_wrong_improved_correct,
        "Improved wrong": both_wrong,
    },
]

print_table(mcnemar_matrix, ["Raw", "Improved correct", "Improved wrong"])

b = raw_correct_improved_wrong
c = raw_wrong_improved_correct
p_value = exact_mcnemar_p_value(b, c)

print()
print("b Raw correct / Improved wrong:", b)
print("c Raw wrong / Improved correct:", c)
print("Discordant pairs:", b + c)
print("Exact McNemar p-value:", round(p_value, 6))
"""),
    md("## 7. Accuracy Difference"),
    code("""raw_accuracy = sum(row["raw_correct"] for row in paired) / len(paired)
improved_accuracy = sum(row["improved_correct"] for row in paired) / len(paired)
accuracy_difference = improved_accuracy - raw_accuracy

effect_size = [
    {
        "raw_accuracy": round(raw_accuracy, 4),
        "improved_accuracy": round(improved_accuracy, 4),
        "accuracy_difference_improved_minus_raw": round(accuracy_difference, 4),
        "raw_correct_improved_wrong": raw_correct_improved_wrong,
        "raw_wrong_improved_correct": raw_wrong_improved_correct,
    }
]

print_table(
    effect_size,
    [
        "raw_accuracy",
        "improved_accuracy",
        "accuracy_difference_improved_minus_raw",
        "raw_correct_improved_wrong",
        "raw_wrong_improved_correct",
    ],
)
"""),
    md("## 8. Final Conclusion"),
    code("""raw_kappa = full_metrics[0]["cohen_kappa"]
improved_kappa = full_metrics[1]["cohen_kappa"]

raw_passed = raw_kappa >= KAPPA_THRESHOLD
improved_passed = improved_kappa >= KAPPA_THRESHOLD

print("Raw Cohen's Kappa:", raw_kappa)
print("Improved Cohen's Kappa:", improved_kappa)
print("Target threshold:", KAPPA_THRESHOLD)
print("Raw passed:", raw_passed)
print("Improved passed:", improved_passed)

if not raw_passed and not improved_passed:
    print()
    print("Conclusion:")
    print("The current LLM classification setup did not meet the target agreement threshold.")
else:
    print()
    print("Conclusion:")
    print("At least one dataset version met the target agreement threshold.")
"""),
]


def write_notebook(filename, cells):
    path = RESULTS_DIR / filename
    path.write_text(
        json.dumps(make_notebook(cells), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return path


pilot_path = write_notebook("pilot_analysis.ipynb", pilot_cells)
full_path = write_notebook("full_analysis.ipynb", full_cells)

print("Recreated notebooks:")
print(pilot_path)
print(full_path)

print()
print("Verify with:")
print('Select-String -Path ".\\Results\\pilot_analysis.ipynb",".\\Results\\full_analysis.ipynb" -Pattern "statsmodels|matplotlib|pandas"')
