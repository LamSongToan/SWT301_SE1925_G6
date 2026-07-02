from __future__ import annotations

import argparse
import csv
import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


BASE_DIR = Path(__file__).resolve().parents[1]

MODEL = "gpt-4o-mini-2024-07-18"
PROMPT_VERSION = "v2"

INPUT_COST_PER_1M_TOKENS = 0.15
CACHED_INPUT_COST_PER_1M_TOKENS = 0.075
OUTPUT_COST_PER_1M_TOKENS = 0.60

CONFIG = {
    "raw": {
        "data_dir": BASE_DIR / "Data" / "Raw",
        "results_dir": BASE_DIR / "Results" / "Raw",
        "input_files": {
            "pilot": "pilot_sample_raw.csv",
            "full": "full_sample_raw.csv",
        },
        "output_files": {
            "pilot": "pilot_llm_output_raw.csv",
            "full": "full_llm_output_raw.csv",
        },
        "log_files": {
            "pilot": "pilot_api_log_raw.csv",
            "full": "full_api_log_raw.csv",
        },
    },
    "improved": {
        "data_dir": BASE_DIR / "Data" / "Improved",
        "results_dir": BASE_DIR / "Results" / "Improved",
        "input_files": {
            "pilot": "pilot_sample_improved.csv",
            "full": "full_sample_improved.csv",
        },
        "output_files": {
            "pilot": "pilot_llm_output_improved.csv",
            "full": "full_llm_output_improved.csv",
        },
        "log_files": {
            "pilot": "pilot_api_log_improved.csv",
            "full": "full_api_log_improved.csv",
        },
    },
}

EXCLUDED_REPORT_COLUMNS = {
    "s2r label",
    "s2r_label",
    "label",
    "ground truth",
    "ground_truth",
    "final label",
    "final_label",
    "author 1",
    "author 2",
    "prediction",
    "llm_prediction",

    # Avoid post-hoc / administrative fields that can bias the LLM.
    "resolution",
    "fix version/s",
    "fix versions",
    "confirmation status",
    "status",
    "votes",
    "watch count",
}


def load_env_file() -> None:
    env_path = BASE_DIR / ".env"

    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value


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


def find_issue_key(row: Dict[str, str]) -> str:
    candidates = [
        "issue_key",
        "Issue Key",
        "BUG-ID",
        "bug_id",
        "Bug ID",
        "key",
        "Key",
        "id",
        "ID",
    ]

    lower_map = {column.strip().lower(): column for column in row.keys()}

    for candidate in candidates:
        actual_column = lower_map.get(candidate.lower())

        if actual_column:
            value = row.get(actual_column, "")

            if value and value.strip():
                return normalize_issue_key(value)

    for value in row.values():
        if value and value.strip().startswith("MC-"):
            return normalize_issue_key(value)

    return ""


def build_report_text(row: Dict[str, str]) -> str:
    parts = []

    for key, value in row.items():
        if value is None:
            continue

        clean_key = key.strip()
        clean_value = str(value).strip()

        if not clean_key or not clean_value:
            continue

        if clean_key.lower() in EXCLUDED_REPORT_COLUMNS:
            continue

        parts.append(f"{clean_key}: {clean_value}")

    return "\n".join(parts)


def build_prompt(issue_key: str, report_text: str) -> str:
    return f"""
You are evaluating the reproducibility of a Mojira / Minecraft bug report.

Task:
Classify whether the bug report contains executable Steps to Reproduce.

Allowed labels:
- Executable
- Non-Executable

Use ONLY the bug report content provided below.
Do NOT use administrative or post-hoc issue tracker outcomes such as resolution,
status, confirmation status, votes, or fix version as the basis for the label.

Core definition:
Executable means another person can reasonably attempt to reproduce the bug
from the report because the report gives enough concrete information about:
1. the relevant context or setup,
2. the user action, command, configuration, or condition that triggers the issue,
3. the observed incorrect behavior,
4. and, when needed, the expected behavior.

Important decision rules:
- Do NOT require numbered steps such as "1, 2, 3" for a report to be Executable.
- A short report can still be Executable if the action and failure condition are concrete.
- A report is Non-Executable if it only states a symptom without a reproducible action.
- A report is Non-Executable if it only says something is broken, crashes, does not work,
  or behaves incorrectly without explaining what to do to trigger it.
- A report is Non-Executable if key information is too vague, missing, or only implied
  by the title.
- For Improved reports, do NOT automatically classify the report as Executable just
  because it contains headings such as "Steps to Reproduce", "Observed Behavior",
  "Expected Behavior", or "Environment".
- For Improved reports, inspect the actual content inside those sections. If the
  sections are generic, incomplete, circular, or merely restate the problem, classify
  the report as Non-Executable.
- If the report provides a concrete action but lacks minor details that a Minecraft
  tester could reasonably infer, classify it as Executable.
- If the report would require guessing the main trigger, setup, or action, classify it
  as Non-Executable.

Return only valid JSON using this schema:
{{
  "issue_key": "{issue_key}",
  "s2r_label": "Executable or Non-Executable",
  "reason": "brief explanation based only on the report content"
}}

Bug report:
{report_text}
""".strip()


def parse_json_response(text: str) -> Dict[str, str]:
    clean = text.strip()

    if clean.startswith("```"):
        clean = clean.strip("`")
        clean = clean.replace("json\n", "", 1).replace("JSON\n", "", 1).strip()

    try:
        data = json.loads(clean)
    except json.JSONDecodeError:
        start = clean.find("{")
        end = clean.rfind("}")

        if start == -1 or end == -1 or end <= start:
            raise

        data = json.loads(clean[start : end + 1])

    issue_key = str(data.get("issue_key", "")).strip()
    s2r_label = normalize_label(str(data.get("s2r_label", "")).strip())
    reason = str(data.get("reason", "")).strip()

    if s2r_label not in {"Executable", "Non-Executable"}:
        raise ValueError(f"Invalid label returned by LLM: {s2r_label}")

    return {
        "issue_key": issue_key,
        "s2r_label": s2r_label,
        "reason": reason,
    }


def get_cached_input_tokens(usage: Any) -> int:
    if not usage:
        return 0

    prompt_tokens_details = getattr(usage, "prompt_tokens_details", None)

    if not prompt_tokens_details:
        return 0

    cached_tokens = getattr(prompt_tokens_details, "cached_tokens", 0)

    return int(cached_tokens or 0)


def calculate_cost_usd(
    input_tokens: int,
    cached_input_tokens: int,
    output_tokens: int,
) -> float:
    uncached_input_tokens = max(input_tokens - cached_input_tokens, 0)

    return (
        uncached_input_tokens * INPUT_COST_PER_1M_TOKENS / 1_000_000
        + cached_input_tokens * CACHED_INPUT_COST_PER_1M_TOKENS / 1_000_000
        + output_tokens * OUTPUT_COST_PER_1M_TOKENS / 1_000_000
    )


def call_openai(prompt: str) -> Dict[str, Any]:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError(
            "The openai package is not installed. Run: pip install openai"
        ) from exc

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Add it to .env or environment variables."
        )

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict but balanced bug report reproducibility "
                    "classifier. Return only valid JSON."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    raw_response = response.choices[0].message.content or ""
    parsed_response = parse_json_response(raw_response)

    usage = response.usage

    input_tokens = usage.prompt_tokens if usage else 0
    output_tokens = usage.completion_tokens if usage else 0
    total_tokens = usage.total_tokens if usage else input_tokens + output_tokens
    cached_input_tokens = get_cached_input_tokens(usage)

    cost_usd = calculate_cost_usd(
        input_tokens=input_tokens,
        cached_input_tokens=cached_input_tokens,
        output_tokens=output_tokens,
    )

    return {
        "parsed_response": parsed_response,
        "raw_response": raw_response,
        "input_tokens": input_tokens,
        "cached_input_tokens": cached_input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "cost_usd": cost_usd,
    }


def write_output_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    fieldnames = [
        "issue_key",
        "s2r_label",
        "reason",
        "status",
        "model",
        "prompt_version",
        "input_tokens",
        "cached_input_tokens",
        "output_tokens",
        "total_tokens",
        "cost_usd",
        "timestamp",
        "raw_response",
    ]

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_api_log_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    fieldnames = [
        "timestamp",
        "version",
        "phase",
        "row_index",
        "total_rows",
        "issue_key",
        "status",
        "prediction",
        "reason",
        "error_message",
        "model",
        "prompt_version",
        "input_tokens",
        "cached_input_tokens",
        "output_tokens",
        "total_tokens",
        "cost_usd",
    ]

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def run_experiment(version: str, phase: str, limit: Optional[int]) -> None:
    load_env_file()

    config = CONFIG[version]

    data_dir = config["data_dir"]
    results_dir = config["results_dir"]

    input_file = data_dir / config["input_files"][phase]
    output_file = results_dir / config["output_files"][phase]
    log_file = results_dir / config["log_files"][phase]

    if not input_file.exists():
        raise FileNotFoundError(f"Cannot find input file: {input_file}")

    rows = read_csv_dicts(input_file)

    if limit is not None:
        rows = rows[:limit]

    output_rows = []
    api_log_rows = []

    total_input_tokens = 0
    total_cached_input_tokens = 0
    total_output_tokens = 0
    total_tokens = 0
    total_cost_usd = 0.0

    print(f"Starting {version} {phase} LLM experiment...")
    print(f"Model      : {MODEL}")
    print(f"Prompt     : {PROMPT_VERSION}")
    print(f"Input file : {input_file}")
    print(f"Output file: {output_file}")
    print(f"Log file   : {log_file}")
    print(f"Total rows : {len(rows)}")
    print("-" * 60)

    for index, row in enumerate(rows, start=1):
        issue_key = find_issue_key(row)

        if not issue_key:
            issue_key = f"row_{index}"

        report_text = build_report_text(row)
        prompt = build_prompt(issue_key, report_text)

        timestamp = datetime.now().isoformat(timespec="seconds")

        print(f"[{index}/{len(rows)}] Processing {issue_key}...")

        try:
            result = call_openai(prompt)

            parsed_response = result["parsed_response"]

            predicted_issue_key = parsed_response["issue_key"] or issue_key
            predicted_label = parsed_response["s2r_label"]
            reason = parsed_response["reason"]

            input_tokens = int(result["input_tokens"])
            cached_input_tokens = int(result["cached_input_tokens"])
            output_tokens = int(result["output_tokens"])
            row_total_tokens = int(result["total_tokens"])
            cost_usd = float(result["cost_usd"])

            total_input_tokens += input_tokens
            total_cached_input_tokens += cached_input_tokens
            total_output_tokens += output_tokens
            total_tokens += row_total_tokens
            total_cost_usd += cost_usd

            output_row = {
                "issue_key": predicted_issue_key,
                "s2r_label": predicted_label,
                "reason": reason,
                "status": "valid_json",
                "model": MODEL,
                "prompt_version": PROMPT_VERSION,
                "input_tokens": input_tokens,
                "cached_input_tokens": cached_input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": row_total_tokens,
                "cost_usd": f"{cost_usd:.8f}",
                "timestamp": timestamp,
                "raw_response": result["raw_response"],
            }

            api_log_row = {
                "timestamp": timestamp,
                "version": version,
                "phase": phase,
                "row_index": index,
                "total_rows": len(rows),
                "issue_key": predicted_issue_key,
                "status": "valid_json",
                "prediction": predicted_label,
                "reason": reason,
                "error_message": "",
                "model": MODEL,
                "prompt_version": PROMPT_VERSION,
                "input_tokens": input_tokens,
                "cached_input_tokens": cached_input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": row_total_tokens,
                "cost_usd": f"{cost_usd:.8f}",
            }

            print("  Status: valid_json")
            print(f"  Prediction: {predicted_label}")
            print(f"  Input tokens : {input_tokens}")
            print(f"  Cached input : {cached_input_tokens}")
            print(f"  Output tokens: {output_tokens}")
            print(f"  Cost/call    : ${cost_usd:.8f}")

        except Exception as exc:
            output_row = {
                "issue_key": issue_key,
                "s2r_label": "",
                "reason": str(exc),
                "status": "error",
                "model": MODEL,
                "prompt_version": PROMPT_VERSION,
                "input_tokens": 0,
                "cached_input_tokens": 0,
                "output_tokens": 0,
                "total_tokens": 0,
                "cost_usd": "0.00000000",
                "timestamp": timestamp,
                "raw_response": "",
            }

            api_log_row = {
                "timestamp": timestamp,
                "version": version,
                "phase": phase,
                "row_index": index,
                "total_rows": len(rows),
                "issue_key": issue_key,
                "status": "error",
                "prediction": "",
                "reason": "",
                "error_message": str(exc),
                "model": MODEL,
                "prompt_version": PROMPT_VERSION,
                "input_tokens": 0,
                "cached_input_tokens": 0,
                "output_tokens": 0,
                "total_tokens": 0,
                "cost_usd": "0.00000000",
            }

            print("  Status: error")
            print(f"  Error: {exc}")

        output_rows.append(output_row)
        api_log_rows.append(api_log_row)

        time.sleep(0.2)

    write_output_csv(output_file, output_rows)
    write_api_log_csv(log_file, api_log_rows)

    print("-" * 60)
    print(f"Saved output to: {output_file}")
    print(f"Saved API log to: {log_file}")
    print(f"Total input tokens        : {total_input_tokens}")
    print(f"Total cached input tokens : {total_cached_input_tokens}")
    print(f"Total output tokens       : {total_output_tokens}")
    print(f"Total tokens              : {total_tokens}")
    print(f"Total cost USD            : ${total_cost_usd:.8f}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run LLM reproducibility classification for Raw or Improved bug reports."
    )

    parser.add_argument(
        "--version",
        required=True,
        choices=["raw", "improved"],
        help="Dataset version to process.",
    )

    parser.add_argument(
        "--phase",
        required=True,
        choices=["pilot", "full"],
        help="Experiment phase to run.",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional row limit for testing.",
    )

    args = parser.parse_args()

    run_experiment(
        version=args.version,
        phase=args.phase,
        limit=args.limit,
    )


if __name__ == "__main__":
    main()
