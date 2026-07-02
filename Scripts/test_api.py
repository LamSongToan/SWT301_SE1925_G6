from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path
from typing import Any, Dict, List


BASE_DIR = Path(__file__).resolve().parents[1]

MODEL = "gpt-4o-mini-2024-07-18"

INPUT_COST_PER_1M_TOKENS = 0.15
OUTPUT_COST_PER_1M_TOKENS = 0.60

CONFIG = {
    "raw": {
        "data_dir": BASE_DIR / "Data" / "Raw",
        "sample_file": "pilot_sample_raw.csv",
    },
    "improved": {
        "data_dir": BASE_DIR / "Data" / "Improved",
        "sample_file": "pilot_sample_improved.csv",
    },
}

LABEL_COLUMNS = {
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
    return (
        value.strip()
        .replace(" Raw", "")
        .replace(" Improved", "")
        .replace("_raw", "")
        .replace("_improved", "")
        .strip()
    )


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

        if not clean_value:
            continue

        if clean_key.lower() in LABEL_COLUMNS:
            continue

        parts.append(f"{clean_key}: {clean_value}")

    return "\n".join(parts)


def build_prompt(issue_key: str, report_text: str) -> str:
    return f"""
You are evaluating the reproducibility of a Mojira / Minecraft bug report.

Task:
Classify whether the bug report has executable Steps to Reproduce.

Allowed labels:
- Executable
- Non-Executable

Definition:
Executable means the report provides enough concrete information for another
person to follow the steps and attempt to reproduce the bug.

Non-Executable means the report does not provide clear, concrete, or sufficient
steps to reproduce the bug.

Return only valid JSON using this schema:
{{
  "issue_key": "{issue_key}",
  "s2r_label": "Executable or Non-Executable",
  "reason": "brief explanation"
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
    s2r_label = str(data.get("s2r_label", "")).strip()
    reason = str(data.get("reason", "")).strip()

    if s2r_label not in {"Executable", "Non-Executable"}:
        raise ValueError(f"Invalid label returned by LLM: {s2r_label}")

    return {
        "issue_key": issue_key,
        "s2r_label": s2r_label,
        "reason": reason,
    }


def calculate_cost_usd(input_tokens: int, output_tokens: int) -> float:
    return (
        input_tokens * INPUT_COST_PER_1M_TOKENS / 1_000_000
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
                    "You are a strict bug report reproducibility classifier. "
                    "Return only valid JSON."
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

    cost_usd = calculate_cost_usd(input_tokens, output_tokens)

    return {
        "parsed_response": parsed_response,
        "raw_response": raw_response,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "cost_usd": cost_usd,
    }


def run_test(version: str, row_index: int) -> None:
    load_env_file()

    config = CONFIG[version]
    sample_file = config["data_dir"] / config["sample_file"]

    if not sample_file.exists():
        raise FileNotFoundError(f"Cannot find sample file: {sample_file}")

    rows = read_csv_dicts(sample_file)

    if not rows:
        raise ValueError(f"Sample file is empty: {sample_file}")

    if row_index < 1 or row_index > len(rows):
        raise ValueError(f"row_index must be between 1 and {len(rows)}")

    row = rows[row_index - 1]

    issue_key = find_issue_key(row)

    if not issue_key:
        issue_key = f"row_{row_index}"

    report_text = build_report_text(row)
    prompt = build_prompt(issue_key, report_text)

    print(f"Loaded test report: {issue_key}")
    print(f"Version: {version}")
    print(f"Model: {MODEL}")
    print(f"Sample file: {sample_file}")
    print("Sending test request to OpenAI API...")

    result = call_openai(prompt)

    parsed_output = {
        "issue_key": result["parsed_response"]["issue_key"] or issue_key,
        "s2r_label": result["parsed_response"]["s2r_label"],
        "reason": result["parsed_response"]["reason"],
    }

    print("-" * 60)
    print("LLM parsed JSON output:")
    print("-" * 60)
    print(json.dumps(parsed_output, ensure_ascii=False, indent=2))
    print("-" * 60)
    print(f"Input tokens : {result['input_tokens']}")
    print(f"Output tokens: {result['output_tokens']}")
    print(f"Total tokens : {result['total_tokens']}")
    print(f"Cost/call    : ${result['cost_usd']:.8f}")
    print("-" * 60)
    print("test_api.py completed successfully.")
    print("No test_api output file was created.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run one OpenAI API test call for Raw or Improved pilot data."
    )

    parser.add_argument(
        "--version",
        choices=["raw", "improved"],
        default="raw",
        help="Dataset version to test.",
    )

    parser.add_argument(
        "--row-index",
        type=int,
        default=1,
        help="1-based row index from the pilot sample file.",
    )

    args = parser.parse_args()

    run_test(args.version, args.row_index)


if __name__ == "__main__":
    main()