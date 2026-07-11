from __future__ import annotations

import argparse
import json
from pathlib import Path

from run_experiment import (
    MODEL,
    EXPERIMENT_SEED,
    APPLY_CONSISTENCY_RULES_BY_PHASE,
    apply_phase_consistency_rules,
    CONFIG,
    RAW_CONTEXT_FILES,
    get_prompt_config,
    call_openai,
    load_env_file,
    read_csv_dicts,
    find_issue_key,
    load_raw_context_rows,
    build_contextual_report_text,
    build_prompt,
)


def run_test(version: str, row_index: int, phase: str) -> None:
    """
    Run one OpenAI API test call using the same prompt-building path as
    run_experiment.py.

    This avoids the old mismatch where test_api.py used Prompts_V1.txt while the
    main experiment used Prompts_Raw_Final.txt / Prompts_Improved_Final.txt.
    """
    load_env_file()

    config = CONFIG[version]
    input_file = config["data_dir"] / config["input_files"][phase]

    if not input_file.exists():
        raise FileNotFoundError(f"Cannot find input file: {input_file}")

    rows = read_csv_dicts(input_file)

    if not rows:
        raise ValueError(f"Input file is empty: {input_file}")

    if row_index < 1 or row_index > len(rows):
        raise ValueError(f"row_index must be between 1 and {len(rows)}")

    raw_context_rows = {}
    if version == "improved":
        raw_context_rows = load_raw_context_rows(phase)

    row = rows[row_index - 1]
    issue_key = find_issue_key(row) or f"row_{row_index}"

    prompt_config = get_prompt_config(version, phase)
    prompt_version = prompt_config["version"]
    prompt_file = prompt_config["file"]

    report_text = build_contextual_report_text(
        version=version,
        row=row,
        issue_key=issue_key,
        raw_context_rows=raw_context_rows,
    )

    system_prompt, user_prompt = build_prompt(issue_key, report_text, prompt_file)

    print(f"Loaded test report: {issue_key}")
    print(f"Version: {version}")
    print(f"Phase: {phase}")
    print(f"Model: {MODEL}")
    print(f"Seed: {EXPERIMENT_SEED}")
    rules_enabled = APPLY_CONSISTENCY_RULES_BY_PHASE.get(phase, False)
    print(f"Post-check rules: {'enabled' if rules_enabled else 'disabled'}")
    print(f"Input file: {input_file}")
    if version == "improved":
        print(f"Raw context: {RAW_CONTEXT_FILES[phase]}")
    print(f"Prompt: {prompt_version}")
    print(f"Prompt file: {prompt_file}")
    print("Sending test request to OpenAI API...")

    result = call_openai(system_prompt, user_prompt)
    parsed_output = result["parsed_response"]

    parsed_output = apply_phase_consistency_rules(
        phase=phase,
        version=version,
        row=row,
        parsed_response=parsed_output,
    )
    result["parsed_response"] = parsed_output

    if not parsed_output.get("issue_key"):
        parsed_output["issue_key"] = issue_key

    print("-" * 60)
    print("LLM parsed JSON output:")
    print("-" * 60)
    print(json.dumps(parsed_output, ensure_ascii=False, indent=2))
    print("-" * 60)
    print(f"Input tokens        : {result['input_tokens']}")
    print(f"Cached input tokens : {result['cached_input_tokens']}")
    print(f"Output tokens       : {result['output_tokens']}")
    print(f"Total tokens        : {result['total_tokens']}")
    print(f"Cost/call           : ${result['cost_usd']:.8f}")
    print(f"Seed                : {result.get('seed', EXPERIMENT_SEED)}")
    print(
        "System fingerprint  : "
        f"{result.get('system_fingerprint', '')}"
    )
    print("-" * 60)
    print("test_api.py completed successfully.")
    print("No test_api output file was created.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run one OpenAI API test call using the same prompt path as run_experiment.py."
    )

    parser.add_argument(
        "--version",
        choices=["raw", "improved"],
        default="raw",
        help="Dataset version to test.",
    )

    parser.add_argument(
        "--phase",
        choices=["pilot", "full"],
        default="pilot",
        help="Dataset phase to test.",
    )

    parser.add_argument(
        "--row-index",
        type=int,
        default=1,
        help="1-based row index from the selected input file.",
    )

    args = parser.parse_args()
    run_test(args.version, args.row_index, args.phase)


if __name__ == "__main__":
    main()
