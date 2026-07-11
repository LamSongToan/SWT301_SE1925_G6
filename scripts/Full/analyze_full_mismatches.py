from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


BASE_DIR = Path(__file__).resolve().parents[1]

INPUTS = {
    "Raw": BASE_DIR / "Results" / "Raw" / "mismatch_analysis_full_raw.csv",
    "Improved": BASE_DIR / "Results" / "Improved" / "mismatch_analysis_full_improved.csv",
}

OUTPUT_DIR = BASE_DIR / "Development" / "Full_Set_V1" / "Analysis"


def normalize_header(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value or "").strip().lower()).strip("_")


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def find_column(row: Dict[str, str], candidates: Iterable[str]) -> str:
    normalized = {normalize_header(key): key for key in row.keys()}
    for candidate in candidates:
        key = normalized.get(normalize_header(candidate))
        if key:
            return key
    return ""


def clean_label(value: str) -> str:
    text = str(value or "").strip().lower().replace("_", " ").replace("-", " ")
    text = " ".join(text.split())
    if text == "executable":
        return "Executable"
    if text in {"non executable", "nonexecutabale", "non executable"}:
        return "Non-Executable"
    return str(value or "").strip()


def error_direction(ground_truth: str, prediction: str) -> str:
    gt = clean_label(ground_truth)
    pred = clean_label(prediction)

    if gt == "Non-Executable" and pred == "Executable":
        return "False Positive"
    if gt == "Executable" and pred == "Non-Executable":
        return "False Negative"
    if not pred:
        return "Invalid / Missing Prediction"
    return "Other"


KEYWORD_GROUPS: List[Tuple[str, Tuple[str, ...]]] = [
    (
        "Missing setup or environment",
        (
            "setup",
            "environment",
            "configuration",
            "settings",
            "version",
            "device",
            "operating system",
            "launcher",
            "network",
            "server",
            "client",
            "world",
            "game mode",
            "gamemode",
            "permission",
            "account",
        ),
    ),
    (
        "Missing trigger, action, or timing",
        (
            "trigger",
            "action",
            "timing",
            "sequence",
            "exact moment",
            "when",
            "how to",
            "critical action",
            "condition",
            "precondition",
            "activate",
            "activation",
        ),
    ),
    (
        "Ambiguous layout, state, or orientation",
        (
            "layout",
            "orientation",
            "direction",
            "state",
            "position",
            "placement",
            "distance",
            "height",
            "location",
            "ambiguous",
            "unclear",
        ),
    ),
    (
        "Wrong or impossible information",
        (
            "invalid command",
            "not a valid command",
            "impossible",
            "contradict",
            "wrong information",
            "incorrect",
            "cannot",
            "not available",
        ),
    ),
    (
        "External dependency or configuration",
        (
            "discord",
            "http",
            "https",
            "internet",
            "network",
            "driver",
            "gpu",
            "resource pack",
            "shader",
            "plugin",
            "mod",
            "datapack",
            "data pack",
        ),
    ),
    (
        "Rendering, audio, or performance",
        (
            "render",
            "visual",
            "animation",
            "audio",
            "music",
            "jukebox",
            "freeze",
            "lag",
            "stutter",
            "fps",
            "fullscreen",
        ),
    ),
    (
        "Command, redstone, or game-mechanics detail",
        (
            "command",
            "redstone",
            "rail",
            "piston",
            "blockstate",
            "block state",
            "loot table",
            "entity data",
            "nbt",
            "spawn",
            "oxid",
            "hitbox",
        ),
    ),
]


def infer_taxonomy(reason: str) -> Tuple[str, str]:
    text = str(reason or "").strip().lower()
    matched: List[str] = []

    for category, keywords in KEYWORD_GROUPS:
        if any(keyword in text for keyword in keywords):
            matched.append(category)

    if not matched:
        return "Other / Manual review required", ""

    return matched[0], " | ".join(matched)


def top_terms(reasons: Iterable[str], limit: int = 30) -> List[Tuple[str, int]]:
    stopwords = {
        "the", "and", "for", "that", "this", "with", "from", "into", "when",
        "under", "which", "they", "their", "there", "does", "do", "not", "are",
        "is", "to", "of", "a", "an", "in", "on", "or", "as", "be", "it",
        "bug", "issue", "report", "steps", "step", "reproduce", "reproduction",
        "information", "provide", "provides", "provided", "needed", "necessary",
        "specific", "clearly", "clear", "critical", "exact", "behavior",
    }

    counter: Counter[str] = Counter()
    for reason in reasons:
        words = re.findall(r"[a-z][a-z0-9_/-]{2,}", str(reason or "").lower())
        counter.update(word for word in words if word not in stopwords)

    return counter.most_common(limit)


def analyze_dataset(dataset: str, path: Path) -> Tuple[List[Dict[str, str]], Counter, Counter]:
    if not path.exists():
        raise FileNotFoundError(f"Cannot find mismatch file: {path}")

    rows = read_csv(path)
    if not rows:
        raise ValueError(f"Mismatch file has no rows: {path}")

    sample = rows[0]

    issue_col = find_column(sample, ["issue_key", "issue key", "bug_id", "key"])
    gt_col = find_column(sample, ["ground_truth", "ground truth", "actual", "true_label"])
    pred_col = find_column(sample, ["prediction", "predicted_label", "llm_prediction"])
    failure_col = find_column(sample, ["s2r_failure_type", "failure_type"])
    reason_col = find_column(sample, ["s2r_reason", "reason"])

    required = {
        "ground truth": gt_col,
        "prediction": pred_col,
    }
    missing = [name for name, column in required.items() if not column]
    if missing:
        raise ValueError(
            f"{path.name} is missing required columns: {', '.join(missing)}"
        )

    output_rows: List[Dict[str, str]] = []
    direction_counts: Counter[str] = Counter()
    taxonomy_counts: Counter[str] = Counter()

    for row in rows:
        issue_key = str(row.get(issue_col, "") if issue_col else "").strip()
        ground_truth = clean_label(row.get(gt_col, ""))
        prediction = clean_label(row.get(pred_col, ""))
        failure_type = str(row.get(failure_col, "") if failure_col else "").strip()
        reason = str(row.get(reason_col, "") if reason_col else "").strip()

        direction = error_direction(ground_truth, prediction)
        primary_category, matched_categories = infer_taxonomy(reason)

        direction_counts[direction] += 1
        taxonomy_counts[primary_category] += 1

        output_rows.append(
            {
                "dataset": dataset,
                "issue_key": issue_key,
                "ground_truth": ground_truth,
                "prediction": prediction,
                "error_direction": direction,
                "s2r_failure_type": failure_type,
                "primary_taxonomy": primary_category,
                "matched_taxonomies": matched_categories,
                "s2r_reason": reason,
                "manual_review_status": "Pending",
                "review_notes": "",
            }
        )

    return output_rows, direction_counts, taxonomy_counts


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return

    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()), quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    summary_rows: List[Dict[str, str]] = []
    all_reasons: List[Tuple[str, str]] = []

    for dataset, path in INPUTS.items():
        analyzed, direction_counts, taxonomy_counts = analyze_dataset(dataset, path)

        write_csv(
            OUTPUT_DIR / f"full_mismatch_taxonomy_{dataset.lower()}.csv",
            analyzed,
        )

        for direction, count in sorted(direction_counts.items()):
            summary_rows.append(
                {
                    "dataset": dataset,
                    "summary_type": "error_direction",
                    "category": direction,
                    "count": str(count),
                }
            )

        for category, count in taxonomy_counts.most_common():
            summary_rows.append(
                {
                    "dataset": dataset,
                    "summary_type": "heuristic_taxonomy",
                    "category": category,
                    "count": str(count),
                }
            )

        all_reasons.extend((dataset, row["s2r_reason"]) for row in analyzed)

    write_csv(OUTPUT_DIR / "full_mismatch_summary.csv", summary_rows)

    term_rows: List[Dict[str, str]] = []
    for dataset in INPUTS:
        reasons = [reason for item_dataset, reason in all_reasons if item_dataset == dataset]
        for term, count in top_terms(reasons):
            term_rows.append(
                {
                    "dataset": dataset,
                    "term": term,
                    "count": str(count),
                }
            )

    write_csv(OUTPUT_DIR / "full_mismatch_top_terms.csv", term_rows)

    print("Full mismatch analysis completed.")
    print(f"Output directory: {OUTPUT_DIR}")
    print("Generated files:")
    print("  - full_mismatch_taxonomy_raw.csv")
    print("  - full_mismatch_taxonomy_improved.csv")
    print("  - full_mismatch_summary.csv")
    print("  - full_mismatch_top_terms.csv")
    print("")
    print("Important: heuristic taxonomy must be manually reviewed before prompt changes.")


if __name__ == "__main__":
    main()
