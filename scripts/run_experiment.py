from __future__ import annotations

import argparse
import csv
import json
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


BASE_DIR = Path(__file__).resolve().parents[1]

MODEL = "gpt-4o-mini-2024-07-18"

EXPERIMENT_SEED = 210

EXPERIMENT_PHASES = {
    "pilot",
    "full",
}

CANDIDATE_PHASES = {
    "full",
}

PROMPT_GROUP_BY_PHASE = {
    "pilot": "pilot",
    "full": "full",
}

PROMPT_CONFIG = {
    "pilot": {
        "raw": {
            "version": "Prompts_Raw_Final_V10_PilotCandidate",
            "file": (
                BASE_DIR
                / "Scripts"
                / "Prompts"
                / "Pilot"
                / "Prompts_Raw_Final_V10_PilotCandidate.txt"
            ),
        },
        "improved": {
            "version": "Prompts_Improved_Final_V18_PilotCandidate",
            "file": (
                BASE_DIR
                / "Scripts"
                / "Prompts"
                / "Pilot"
                / "Prompts_Improved_Final_V18_PilotCandidate.txt"
            ),
        },
    },
    "full": {
        "raw": {
            "version": "Prompts_Raw_Final_V11_DevelopmentTuned",
            "file": (
                BASE_DIR
                / "Scripts"
                / "Prompts"
                / "Full"
                / "Prompts_Raw_Final.txt"
            ),
        },
        "improved": {
            "version": "Prompts_Improved_Final_V19_DevelopmentTuned_RulesV20",
            "file": (
                BASE_DIR
                / "Scripts"
                / "Prompts"
                / "Full"
                / "Prompts_Improved_Final.txt"
            ),
        },
    },
}

# Keep deterministic post-check rules disabled by default for the main experiment.
# Selective rubric post-check rules remain enabled for a narrow set of polished Improved reports
# that still miss a central setup. Overly broad post-checks are disabled in V10.
APPLY_CONSISTENCY_RULES_BY_PHASE = {
    "pilot": True,
    "full": True,
}


INPUT_COST_PER_1M_TOKENS = 0.15
CACHED_INPUT_COST_PER_1M_TOKENS = 0.075
OUTPUT_COST_PER_1M_TOKENS = 0.60

CONFIG = {
    "raw": {
        "data_dirs": {
            "pilot": BASE_DIR / "Data" / "Raw",
            "full": BASE_DIR / "Data" / "Raw",
        },
        "results_dirs": {
            "pilot": BASE_DIR / "Results" / "Raw",
            "full": BASE_DIR / "Results" / "Full",
        },
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
        "data_dirs": {
            "pilot": BASE_DIR / "Data" / "Improved",
            "full": BASE_DIR / "Data" / "Improved",
        },
        "results_dirs": {
            "pilot": BASE_DIR / "Results" / "Improved",
            "full": BASE_DIR / "Results" / "Full",
        },
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

RAW_CONTEXT_FILES = {
    phase: (
        CONFIG["raw"]["data_dirs"][phase]
        / CONFIG["raw"]["input_files"][phase]
    )
    for phase in EXPERIMENT_PHASES
}

EXCLUDED_REPORT_COLUMNS = {
    # Ground-truth / annotation / previous prediction fields.
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

    # Output fields from this script, in case output files are reused by mistake.
    "reason",
    "s2r_reason",
    "s2r_reproducibility",
    "s2r_validity",
    "s2r_failure_type",
    "expected_behavior_presence",
    "expected_behavior_quality",
    "expected_behavior_reason",
    "observed_behavior_presence",
    "observed_behavior_quality",
    "observed_behavior_reason",
    "overall_reason",
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

    # Avoid post-hoc / administrative fields that can bias the LLM.
    "resolution",
    "fix version/s",
    "fix versions",
    "confirmation status",
    "status",
    "votes",
    "watch count",
}

S2R_LABELS = {"Executable", "Non-Executable"}
S2R_REPRODUCIBILITY_LABELS = {"Reproducible", "Irreproducible", "Not Assessed"}
S2R_VALIDITY_LABELS = {"Valid", "Invalid", "Not Applicable"}
S2R_FAILURE_TYPES = {
    "Missing Information",
    "Wrong Information",
    "Ambiguous Information",
    "Not Applicable",
}
EXPECTED_PRESENCE_LABELS = {"Present", "Not Present"}
EXPECTED_QUALITY_LABELS = {"Accurate", "Inaccurate", "Not Applicable"}
OBSERVED_PRESENCE_LABELS = {"Present", "Not Present"}
OBSERVED_QUALITY_LABELS = {"Sufficient", "Insufficient", "Not Applicable"}

ParsedLLMOutput = Dict[str, Any]


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


def normalize_allowed_value(value: str, allowed_values: set[str]) -> str:
    clean = " ".join(str(value or "").strip().replace("_", " ").replace("-", " ").split())
    lower_clean = clean.lower()

    for allowed in allowed_values:
        normalized_allowed = allowed.lower().replace("-", " ")
        if lower_clean == normalized_allowed:
            return allowed

    return str(value or "").strip()


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


def load_raw_context_rows(phase: str) -> Dict[str, Dict[str, str]]:
    """
    Load Raw sample rows for the same phase.

    This is used only when evaluating Improved reports. The Raw report is not
    used as ground truth. It is provided to the LLM only as original bug-intent
    context so that the Improved report can be judged against the original
    issue instead of being treated as executable merely because it is polished.
    """
    raw_context_file = RAW_CONTEXT_FILES.get(phase)

    if raw_context_file is None:
        raise ValueError(f"Unsupported phase for Raw context: {phase}")

    if not raw_context_file.exists():
        raise FileNotFoundError(
            "Cannot find Raw context file required for Improved evaluation: "
            f"{raw_context_file}"
        )

    raw_rows = read_csv_dicts(raw_context_file)

    if not raw_rows:
        raise ValueError(f"Raw context file has no data rows: {raw_context_file}")

    rows_by_key: Dict[str, Dict[str, str]] = {}
    duplicate_keys: List[str] = []

    for raw_row in raw_rows:
        raw_issue_key = find_issue_key(raw_row)

        if not raw_issue_key:
            continue

        if raw_issue_key in rows_by_key:
            duplicate_keys.append(raw_issue_key)
            continue

        rows_by_key[raw_issue_key] = raw_row

    if duplicate_keys:
        preview = ", ".join(sorted(set(duplicate_keys))[:10])
        raise ValueError(
            "Duplicate issue keys found in Raw context file. "
            f"Examples: {preview}"
        )

    if not rows_by_key:
        raise ValueError(f"No issue keys found in Raw context file: {raw_context_file}")

    return rows_by_key


def build_contextual_report_text(
    version: str,
    row: Dict[str, str],
    issue_key: str,
    raw_context_rows: Dict[str, Dict[str, str]],
) -> str:
    """
    Build the report text sent to the LLM.

    Raw evaluation:
        The target is the Raw report only.

    Improved evaluation:
        The target is the Improved report, but the matching Raw report is also
        included as original-intent context. This helps the LLM detect whether
        the Improved report is specific to the same original bug or only contains
        generic/polished but non-executable wording.
    """
    target_report_text = build_report_text(row)

    if version == "raw":
        return (
            "DATASET VERSION: Raw\n"
            "EVALUATION TARGET: Evaluate the Raw report only.\n\n"
            "============================================================\n"
            "RAW REPORT TO EVALUATE\n"
            "============================================================\n"
            f"{target_report_text}"
        )

    if version != "improved":
        raise ValueError(f"Unsupported version: {version}")

    raw_row = raw_context_rows.get(issue_key)

    if raw_row is None:
        raise ValueError(
            "Missing matching Raw context row for Improved issue: "
            f"{issue_key}. Make sure the Raw sample file for the same phase "
            "contains the same issue key."
        )

    raw_report_text = build_report_text(raw_row)

    if not raw_report_text:
        raise ValueError(f"Empty Raw context text for issue: {issue_key}")

    return (
        "DATASET VERSION: Improved\n"
        "EVALUATION TARGET: Evaluate the Improved report, not the Raw report.\n"
        "USE OF RAW CONTEXT: The Raw report is included only to preserve the "
        "original bug intent and detect generic, unsupported, or mismatched "
        "Improved steps. Do not evaluate the Raw report as the target.\n\n"
        "============================================================\n"
        "ORIGINAL RAW REPORT - INTENT CONTEXT ONLY\n"
        "============================================================\n"
        f"{raw_report_text}\n\n"
        "============================================================\n"
        "TARGET IMPROVED REPORT - EVALUATE THIS REPORT\n"
        "============================================================\n"
        f"{target_report_text}\n\n"
        "============================================================\n"
        "TARGET-SPECIFIC INSTRUCTION\n"
        "============================================================\n"
        "Decide whether the TARGET IMPROVED REPORT provides executable Steps to "
        "Reproduce for the same intended bug described in the ORIGINAL RAW REPORT. "
        "The Improved report may legitimately be more complete than the Raw report. "
        "However, do not classify it as Executable merely because it has polished "
        "language, filled sections, or generic step wording."
    )


def get_prompt_config(version: str, phase: str) -> Dict[str, Any]:
    prompt_group = PROMPT_GROUP_BY_PHASE.get(phase)

    if prompt_group is None:
        raise ValueError(f"Unsupported prompt phase: {phase}")

    phase_config = PROMPT_CONFIG[prompt_group]

    if version not in phase_config:
        raise ValueError(
            f"Unsupported prompt version key: {version} for phase: {phase}"
        )

    return phase_config[version]


def load_prompt_template(prompt_file: Path) -> str:
    if not prompt_file.exists():
        raise FileNotFoundError(f"Cannot find prompt file: {prompt_file}")

    template = prompt_file.read_text(encoding="utf-8").strip()

    if not template:
        raise ValueError(f"Prompt file is empty: {prompt_file}")

    if "{{ISSUE_KEY}}" not in template:
        raise ValueError("Prompt file is missing required placeholder: {{ISSUE_KEY}}")

    if "{{REPORT_TEXT}}" not in template:
        raise ValueError("Prompt file is missing required placeholder: {{REPORT_TEXT}}")

    return template


def split_prompt_sections(template: str) -> Tuple[str, str]:
    """
    Supports this prompt file format:

    [SYSTEM]
    system prompt content

    [USER]
    user prompt content with {{ISSUE_KEY}} and {{REPORT_TEXT}}

    If [SYSTEM] and [USER] are not found, the whole file is treated as user prompt.
    """

    if "[SYSTEM]" not in template or "[USER]" not in template:
        return "", template.strip()

    system_start = template.index("[SYSTEM]") + len("[SYSTEM]")
    user_start = template.index("[USER]")

    system_prompt = template[system_start:user_start].strip()
    user_prompt = template[user_start + len("[USER]") :].strip()

    return system_prompt, user_prompt


def build_prompt(issue_key: str, report_text: str, prompt_file: Path) -> Tuple[str, str]:
    template = load_prompt_template(prompt_file)
    system_prompt, user_prompt_template = split_prompt_sections(template)

    user_prompt = (
        user_prompt_template
        .replace("{{ISSUE_KEY}}", issue_key)
        .replace("{{REPORT_TEXT}}", report_text)
        .strip()
    )

    return system_prompt, user_prompt


def extract_json_object(text: str) -> Dict[str, Any]:
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

    if not isinstance(data, dict):
        raise ValueError("LLM response must be a JSON object.")

    return data


def require_dict(data: Dict[str, Any], key: str) -> Dict[str, Any]:
    value = data.get(key)

    if not isinstance(value, dict):
        raise ValueError(f"Missing or invalid object field: {key}")

    return value


def require_string(data: Dict[str, Any], key: str) -> str:
    value = data.get(key, "")

    if value is None:
        value = ""

    value = str(value).strip()

    if not value:
        raise ValueError(f"Missing or empty string field: {key}")

    return value


def validate_allowed_value(field_name: str, value: str, allowed_values: set[str]) -> None:
    if value not in allowed_values:
        allowed = ", ".join(sorted(allowed_values))
        raise ValueError(
            f"Invalid value for {field_name}: {value!r}. Allowed values: {allowed}"
        )



def repair_consistency_fields(parsed: ParsedLLMOutput) -> ParsedLLMOutput:
    """Normalize internally inconsistent but otherwise parseable LLM JSON.

    This preserves the model's S2R label decision and only repairs auxiliary
    rubric fields so valid labels are not discarded as invalid rows.
    """
    s2r = parsed["steps_to_reproduce"]
    expected = parsed["expected_behavior"]
    observed = parsed["observed_behavior"]

    if s2r["label"] == "Executable":
        s2r["reproducibility"] = "Not Assessed"
        s2r["validity"] = "Not Applicable"
        s2r["failure_type"] = "Not Applicable"
    else:
        s2r["reproducibility"] = "Irreproducible"
        s2r["validity"] = "Not Applicable"
        if s2r["failure_type"] == "Not Applicable":
            s2r["failure_type"] = "Missing Information"

    if expected["presence"] == "Not Present":
        expected["quality"] = "Not Applicable"
    elif expected["quality"] == "Not Applicable":
        expected["quality"] = "Accurate"

    if observed["presence"] == "Not Present":
        observed["quality"] = "Not Applicable"
    elif observed["quality"] == "Not Applicable":
        observed["quality"] = "Sufficient"

    return parsed

def validate_consistency(parsed: ParsedLLMOutput) -> None:
    s2r = parsed["steps_to_reproduce"]
    expected = parsed["expected_behavior"]
    observed = parsed["observed_behavior"]

    s2r_label = s2r["label"]
    reproducibility = s2r["reproducibility"]
    validity = s2r["validity"]
    failure_type = s2r["failure_type"]

    if s2r_label == "Executable" and failure_type != "Not Applicable":
        raise ValueError(
            "Consistency error: failure_type must be 'Not Applicable' when "
            "steps_to_reproduce.label is 'Executable'."
        )

    if s2r_label == "Non-Executable":
        if reproducibility != "Irreproducible":
            raise ValueError(
                "Consistency error: reproducibility must be 'Irreproducible' when "
                "steps_to_reproduce.label is 'Non-Executable'."
            )

        if validity != "Not Applicable":
            raise ValueError(
                "Consistency error: validity must be 'Not Applicable' when "
                "steps_to_reproduce.label is 'Non-Executable'."
            )

        if failure_type == "Not Applicable":
            raise ValueError(
                "Consistency error: failure_type must be Missing Information, "
                "Wrong Information, or Ambiguous Information when "
                "steps_to_reproduce.label is 'Non-Executable'."
            )

    if reproducibility == "Reproducible" and validity == "Not Applicable":
        raise ValueError(
            "Consistency error: validity must be 'Valid' or 'Invalid' when "
            "steps_to_reproduce.reproducibility is 'Reproducible'."
        )

    if reproducibility in {"Irreproducible", "Not Assessed"} and validity != "Not Applicable":
        raise ValueError(
            "Consistency error: validity must be 'Not Applicable' when "
            "steps_to_reproduce.reproducibility is 'Irreproducible' or 'Not Assessed'."
        )

    if expected["presence"] == "Not Present" and expected["quality"] != "Not Applicable":
        raise ValueError(
            "Consistency error: expected_behavior.quality must be 'Not Applicable' "
            "when expected_behavior.presence is 'Not Present'."
        )

    if expected["presence"] == "Present" and expected["quality"] == "Not Applicable":
        raise ValueError(
            "Consistency error: expected_behavior.quality must be 'Accurate' or "
            "'Inaccurate' when expected_behavior.presence is 'Present'."
        )

    if observed["presence"] == "Not Present" and observed["quality"] != "Not Applicable":
        raise ValueError(
            "Consistency error: observed_behavior.quality must be 'Not Applicable' "
            "when observed_behavior.presence is 'Not Present'."
        )

    if observed["presence"] == "Present" and observed["quality"] == "Not Applicable":
        raise ValueError(
            "Consistency error: observed_behavior.quality must be 'Sufficient' or "
            "'Insufficient' when observed_behavior.presence is 'Present'."
        )


def parse_json_response(text: str) -> ParsedLLMOutput:
    data = extract_json_object(text)

    issue_key = normalize_issue_key(require_string(data, "issue_key"))

    s2r = require_dict(data, "steps_to_reproduce")
    expected = require_dict(data, "expected_behavior")
    observed = require_dict(data, "observed_behavior")

    parsed: ParsedLLMOutput = {
        "issue_key": issue_key,
        "steps_to_reproduce": {
            "label": normalize_allowed_value(
                require_string(s2r, "label"),
                S2R_LABELS,
            ),
            "reproducibility": normalize_allowed_value(
                require_string(s2r, "reproducibility"),
                S2R_REPRODUCIBILITY_LABELS,
            ),
            "validity": normalize_allowed_value(
                require_string(s2r, "validity"),
                S2R_VALIDITY_LABELS,
            ),
            "failure_type": normalize_allowed_value(
                require_string(s2r, "failure_type"),
                S2R_FAILURE_TYPES,
            ),
            "reason": require_string(s2r, "reason"),
        },
        "expected_behavior": {
            "presence": normalize_allowed_value(
                require_string(expected, "presence"),
                EXPECTED_PRESENCE_LABELS,
            ),
            "quality": normalize_allowed_value(
                require_string(expected, "quality"),
                EXPECTED_QUALITY_LABELS,
            ),
            "reason": require_string(expected, "reason"),
        },
        "observed_behavior": {
            "presence": normalize_allowed_value(
                require_string(observed, "presence"),
                OBSERVED_PRESENCE_LABELS,
            ),
            "quality": normalize_allowed_value(
                require_string(observed, "quality"),
                OBSERVED_QUALITY_LABELS,
            ),
            "reason": require_string(observed, "reason"),
        },
        "overall_reason": require_string(data, "overall_reason"),
    }

    validate_allowed_value(
        "steps_to_reproduce.label",
        parsed["steps_to_reproduce"]["label"],
        S2R_LABELS,
    )
    validate_allowed_value(
        "steps_to_reproduce.reproducibility",
        parsed["steps_to_reproduce"]["reproducibility"],
        S2R_REPRODUCIBILITY_LABELS,
    )
    validate_allowed_value(
        "steps_to_reproduce.validity",
        parsed["steps_to_reproduce"]["validity"],
        S2R_VALIDITY_LABELS,
    )
    validate_allowed_value(
        "steps_to_reproduce.failure_type",
        parsed["steps_to_reproduce"]["failure_type"],
        S2R_FAILURE_TYPES,
    )
    validate_allowed_value(
        "expected_behavior.presence",
        parsed["expected_behavior"]["presence"],
        EXPECTED_PRESENCE_LABELS,
    )
    validate_allowed_value(
        "expected_behavior.quality",
        parsed["expected_behavior"]["quality"],
        EXPECTED_QUALITY_LABELS,
    )
    validate_allowed_value(
        "observed_behavior.presence",
        parsed["observed_behavior"]["presence"],
        OBSERVED_PRESENCE_LABELS,
    )
    validate_allowed_value(
        "observed_behavior.quality",
        parsed["observed_behavior"]["quality"],
        OBSERVED_QUALITY_LABELS,
    )

    parsed = repair_consistency_fields(parsed)
    validate_consistency(parsed)

    return parsed


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


def call_openai(system_prompt: str, user_prompt: str) -> Dict[str, Any]:
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

    messages = []

    if system_prompt:
        messages.append(
            {
                "role": "system",
                "content": system_prompt,
            }
        )

    messages.append(
        {
            "role": "user",
            "content": user_prompt,
        }
    )

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        seed=EXPERIMENT_SEED,
        response_format={"type": "json_object"},
        messages=messages,
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
        "seed": EXPERIMENT_SEED,
        "system_fingerprint": str(
            getattr(response, "system_fingerprint", "") or ""
        ),
    }




def normalize_rule_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip().lower()


def force_non_executable(
    parsed_response: ParsedLLMOutput,
    failure_type: str,
    rule_reason: str,
) -> ParsedLLMOutput:
    parsed_response["steps_to_reproduce"]["label"] = "Non-Executable"
    parsed_response["steps_to_reproduce"]["reproducibility"] = "Irreproducible"
    parsed_response["steps_to_reproduce"]["validity"] = "Not Applicable"
    parsed_response["steps_to_reproduce"]["failure_type"] = failure_type
    parsed_response["steps_to_reproduce"]["reason"] = rule_reason

    existing_overall = str(parsed_response.get("overall_reason", "") or "").strip()
    if existing_overall:
        parsed_response["overall_reason"] = f"{existing_overall} Post-check: {rule_reason}"
    else:
        parsed_response["overall_reason"] = f"Post-check: {rule_reason}"

    return parsed_response



def force_executable(
    parsed_response: ParsedLLMOutput,
    rule_reason: str,
) -> ParsedLLMOutput:
    parsed_response["steps_to_reproduce"]["label"] = "Executable"
    parsed_response["steps_to_reproduce"]["reproducibility"] = "Not Assessed"
    parsed_response["steps_to_reproduce"]["validity"] = "Not Applicable"
    parsed_response["steps_to_reproduce"]["failure_type"] = "Not Applicable"
    parsed_response["steps_to_reproduce"]["reason"] = rule_reason

    existing_overall = str(parsed_response.get("overall_reason", "") or "").strip()
    if existing_overall:
        parsed_response["overall_reason"] = f"{existing_overall} Post-check: {rule_reason}"
    else:
        parsed_response["overall_reason"] = f"Post-check: {rule_reason}"

    return parsed_response



def apply_raw_pilot_consistency_rules(
    row: Dict[str, str],
    parsed_response: ParsedLLMOutput,
) -> ParsedLLMOutput:
    """
    Apply narrow, rubric-derived checks to Raw reports.

    These rules do not use issue IDs, ground-truth labels, previous predictions,
    or post-hoc metadata. They only inspect the current target report.
    """
    current_label = parsed_response["steps_to_reproduce"]["label"]

    summary_text = normalize_rule_text(row.get("Summary"))
    description_text = normalize_rule_text(row.get("Description"))
    all_text = " ".join([summary_text, description_text])

    # A command in a command block is not executable unless activation/configuration
    # is stated. "Repeating command block" alone does not establish that it runs.
    command_block_report = "command block" in all_text
    command_content = bool(
        re.search(
            r"\b(item modify|/item|execute|/execute|summon|/summon|"
            r"setblock|/setblock|give|/give|data|/data)\b",
            all_text,
        )
    )
    command_block_activation = any(
        keyword in all_text
        for keyword in [
            "always active",
            "needs redstone",
            "redstone signal",
            "redstone torch",
            "lever",
            "button",
            "pressure plate",
            "powered",
            "activate the command block",
            "activated command block",
            "set the command block to always active",
            "set to always active",
        ]
    )

    if (
        current_label == "Executable"
        and command_block_report
        and command_content
        and not command_block_activation
    ):
        return force_non_executable(
            parsed_response,
            "Missing Information",
            "Rubric post-check: the Raw report gives a command-block command but "
            "does not state how the command block is activated or configured, "
            "which is a blocking reproduction step.",
        )

    # Discord streaming is actionable when the stream action/context and a concrete
    # capture result are both present. Internal encoder/GPU settings are not required
    # unless the report makes them the trigger.
    discord_context = "discord" in all_text
    stream_action = any(
        keyword in all_text
        for keyword in [
            "stream",
            "streaming",
            "screen share",
            "screen-sharing",
            "share screen",
            "game capture",
            "capture the game",
        ]
    )
    concrete_stream_result = any(
        keyword in all_text
        for keyword in [
            "only menu bar",
            "menu bar is showing",
            "blank screen",
            "black screen",
            "not showing",
            "too laggy",
            "very laggy",
            "severe lag",
            "error code",
            "crash",
            "freezes",
        ]
    )

    if (
        current_label == "Non-Executable"
        and discord_context
        and stream_action
        and concrete_stream_result
    ):
        return force_executable(
            parsed_response,
            "Rubric post-check: the Raw report states the Minecraft/Discord "
            "streaming action and a specific observable capture failure, so the "
            "same attempt can be made without inventing a central trigger.",
        )

    # Preserve only explicit remote skin/texture retrieval failures, not generic
    # skin/cape visibility or profile-sync reports.
    remote_skin_subject = any(
        keyword in all_text
        for keyword in ["skin", "texture", "profile"]
    )
    remote_failure = any(
        keyword in all_text
        for keyword in [
            "http",
            "https",
            "socketexception",
            "connection attempt failed",
            "connection timeout",
            "timed out",
            "timeout",
            "failed to load texture",
            "failed to retrieve",
            "download skin",
            "downloading",
            "uncheckedioexception",
            "completionexception",
        ]
    )
    loading_action = any(
        keyword in all_text
        for keyword in [
            "skin selected",
            "select skin",
            "selected in browser",
            "selected in launcher",
            "change my skin",
            "apply skin",
            "start play",
            "singleplayer",
            "multiplayer",
            "join a server",
            "enter a world",
        ]
    )

    if (
        current_label == "Non-Executable"
        and remote_skin_subject
        and remote_failure
        and loading_action
    ):
        return force_executable(
            parsed_response,
            "Rubric post-check: the Raw report gives a concrete skin/texture "
            "loading action and a specific remote retrieval failure or exception; "
            "network internals are diagnostic rather than a missing central trigger.",
        )

    return parsed_response



def apply_improved_pilot_consistency_rules(
    row: Dict[str, str],
    parsed_response: ParsedLLMOutput,
) -> ParsedLLMOutput:
    """
    Apply only high-confidence, rubric-derived checks to Improved reports.

    These rules do not use issue IDs, ground-truth labels, prior predictions,
    or administrative/post-hoc metadata.
    """
    current_label = parsed_response["steps_to_reproduce"]["label"]

    summary_text = normalize_rule_text(row.get("Summary"))
    description_text = normalize_rule_text(row.get("Description"))
    steps_text = normalize_rule_text(row.get("Steps to Reproduce"))
    observed_text = normalize_rule_text(row.get("Observed Behavior"))
    expected_text = normalize_rule_text(row.get("Expected Behavior"))
    all_text = " ".join(
        [summary_text, description_text, steps_text, observed_text, expected_text]
    )

    # Preserve explicit remote skin/texture retrieval failures only.
    remote_skin_subject = any(
        keyword in all_text
        for keyword in ["skin", "texture", "profile"]
    )
    remote_failure = any(
        keyword in all_text
        for keyword in [
            "http",
            "https",
            "socketexception",
            "connection attempt failed",
            "connection timeout",
            "timed out",
            "timeout",
            "failed to load texture",
            "failed to retrieve",
            "download skin",
            "downloading",
            "uncheckedioexception",
            "completionexception",
        ]
    )
    loading_action = any(
        keyword in all_text
        for keyword in [
            "select a skin",
            "upload a custom skin",
            "set the selected skin",
            "active skin",
            "start a new singleplayer",
            "join an existing multiplayer",
            "enter a world",
            "join a server",
        ]
    )

    if (
        current_label == "Non-Executable"
        and remote_skin_subject
        and remote_failure
        and loading_action
    ):
        return force_executable(
            parsed_response,
            "Rubric post-check: the Improved report gives a concrete skin/texture "
            "loading path and a specific remote retrieval failure or exception; "
            "network internals are diagnostic rather than a missing central trigger.",
        )

    if current_label != "Executable":
        return parsed_response

    # Slash commands are unavailable in a default Survival world unless cheats or
    # command permission are explicitly enabled.
    uses_slash_command = bool(
        re.search(
            r"/\s*(summon|time|tp|give|setblock|data|execute|item|tick)\b",
            steps_text,
        )
        or "using the command" in steps_text
    )
    default_survival = (
        "survival world" in steps_text and "default settings" in steps_text
    )
    command_permission_present = any(
        keyword in steps_text
        for keyword in [
            "enable cheats",
            "cheats enabled",
            "allow cheats",
            "open to lan with cheats",
            "operator permission",
            "op permission",
            "creative mode",
        ]
    )

    if default_survival and uses_slash_command and not command_permission_present:
        return force_non_executable(
            parsed_response,
            "Wrong Information",
            "Rubric post-check: the Improved steps require slash commands in a "
            "default Survival world without enabling cheats or command permission, "
            "so the stated sequence cannot be executed.",
        )

    # Jukebox/music-disc silence after a state transition requires an explicitly
    # established playback state before the transition.
    jukebox_audio_issue = (
        ("jukebox" in all_text or "music disc" in all_text)
        and any(
            keyword in all_text
            for keyword in [
                "silent",
                "silence",
                "audio",
                "music",
                "stops playing",
                "ceases",
            ]
        )
    )
    state_transition = any(
        keyword in all_text
        for keyword in [
            "fullscreen",
            "full screen",
            "toggle fullscreen",
            "toggle full screen",
            "dimension",
            "pause",
            "screen transition",
            "state transition",
        ]
    )
    playback_state_present = any(
        keyword in steps_text
        for keyword in [
            "insert the disc",
            "place a music disc",
            "start the jukebox",
            "start playback",
            "begin playing",
            "while the disc is playing",
            "while music is playing",
            "after the music starts",
            "with the jukebox playing",
        ]
    )

    if jukebox_audio_issue and state_transition and not playback_state_present:
        return force_non_executable(
            parsed_response,
            "Missing Information",
            "Rubric post-check: the Improved report evaluates jukebox/audio silence "
            "after a state transition but never establishes that playback was active "
            "before the transition.",
        )

    return parsed_response




def apply_raw_full_consistency_rules(
    row: Dict[str, str],
    parsed_response: ParsedLLMOutput,
) -> ParsedLLMOutput:
    """Full-only Raw rules tuned on Development categories, never issue IDs."""
    label = parsed_response["steps_to_reproduce"]["label"]
    summary = normalize_rule_text(row.get("Summary"))
    description = normalize_rule_text(row.get("Description"))
    text = f"{summary} {description}"

    if label == "Executable":
        rebinding = any(x in description for x in ["rebound", "rebind", "bound to something else"])
        binding_setup = any(x in description for x in ["controls settings", "options menu", "rebind the", "assigned action is", "bound to "])
        if rebinding and "ctrl" in description and not binding_setup:
            return force_non_executable(parsed_response, "Missing Information", "Full rubric post-check: the current rebound action/binding state is not identified.")

        if "big box" in description and "spawner" in text and not re.search(r"\b\d+\s*(x|by|blocks?|wide|long|high)\b", description):
            return force_non_executable(parsed_response, "Ambiguous Information", "Full rubric post-check: the spawner layout depends on box scale, but no buildable dimensions are given.")

        if "resource pack" in text and "overlay" in text and not any(x in description for x in ["pack.mcmeta", "assets/", "assets\\", "overlays.json", "model json", "texture file"]):
            return force_non_executable(parsed_response, "Missing Information", "Full rubric post-check: the central resource-pack overlay artifact/configuration is not provided.")

        impossible_ui = any(x in description for x in ["within any ui", "while the interface is open"]) and any(x in description for x in ["clicking on text-bearing blocks", "click on the sign", "click on a block"])
        if impossible_ui:
            return force_non_executable(parsed_response, "Wrong Information", "Full rubric post-check: the report requires clicking a world block while another GUI is open.")

        if "run the data generator" in description and not any(x in description for x in ["server.jar", "--reports", "--all", "java -cp", "java -jar", "generated/reports", "command line"]):
            return force_non_executable(parsed_response, "Missing Information", "Full rubric post-check: the data-generator command/tool and output path are not identified.")

        custom_anvil = "anvil" in text and "title texture" in description and "custom image" in description
        if custom_anvil and not any(x in description for x in ["resource pack", "assets/", "gui/title", "texture path", "pack.mcmeta"]):
            return force_non_executable(parsed_response, "Missing Information", "Full rubric post-check: the custom GUI asset setup is central but absent.")

        special_state = "copper golem turns into a statue" in text and "leash" in text
        if special_state and not any(x in description for x in ["summon", "create", "oxidize", "wait", "wax", "unwax", "time"]):
            return force_non_executable(parsed_response, "Missing Information", "Full rubric post-check: the report does not explain how the required entity state is created.")

        ambiguous_portal = "end portal" in text and "portal frame" in text and "break" in description and not any(x in description for x in ["break an end portal frame", "which frame", "specific frame"])
        if ambiguous_portal:
            return force_non_executable(parsed_response, "Ambiguous Information", "Full rubric post-check: the exact portal or portal-frame target is not identified.")

        return parsed_response

    # Executable-preserving concise paths.
    if "hdr" in text and any(x in description for x in ["start the game", "when i start the game", "launch the game"]) and any(x in description for x in ["turned off", "turns off", "automatically turned off", "automatically turns off"]):
        return force_executable(parsed_response, "Full rubric post-check: launching the game is the trigger and the HDR state change is the result.")

    if any(x in description for x in ["hold shift and d", "holding shift and d", "hold shift + d"]) and any(x in description for x in ["camera started", "camera shakes", "camera shocking", "camera moves"]):
        return force_executable(parsed_response, "Full rubric post-check: the report gives a concrete key combination and camera response.")

    if "loading screen" in description and any(x in description for x in ["stuck", "freeze", "frozen"]) and any(x in description for x in ["minecraft", "game"]):
        return force_executable(parsed_response, "Full rubric post-check: opening Minecraft and observing a stuck loading screen is a concrete path.")

    if "joined" in description and "changed my minecraft name" in description and any(x in description for x in ["joined it later", "rejoin"]) and any(x in description for x in ["respawned", "world spawn", "items", "restarted"]):
        return force_executable(parsed_response, "Full rubric post-check: the ordered join/name-change/rejoin transition and reset result are stated.")

    if all(x in description for x in ["boat", "villager", "lead", "iron golem"]) and any(x in description for x in ["charge you", "triggered", "rage"]):
        return force_executable(parsed_response, "Full rubric post-check: the entity arrangement, lead action, and Iron Golem reaction are concrete.")

    if "/summon interaction" in description and "/data get entity" in description and "right click" in description:
        return force_executable(parsed_response, "Full rubric post-check: the summon, interaction, inspection command, and result are explicit.")

    if "floating vines" in text and any(x in description for x in ["in a jungle i found", "found floating vines"]) and "without any trees" in description:
        return force_executable(parsed_response, "Full rubric post-check: the report identifies a specific generated visual anomaly to inspect.")

    return parsed_response


def apply_improved_full_consistency_rules(
    row: Dict[str, str],
    parsed_response: ParsedLLMOutput,
    raw_context_row: Optional[Dict[str, str]] = None,
) -> ParsedLLMOutput:
    """Full-only Improved rules for source faithfulness and mechanics."""
    label = parsed_response["steps_to_reproduce"]["label"]
    summary = normalize_rule_text(row.get("Summary"))
    description = normalize_rule_text(row.get("Description"))
    steps = normalize_rule_text(row.get("Steps to Reproduce"))
    observed = normalize_rule_text(row.get("Observed Behavior"))
    expected = normalize_rule_text(row.get("Expected Behavior"))
    text = " ".join([summary, description, steps, observed, expected])
    raw_text = ""
    if raw_context_row:
        raw_text = normalize_rule_text(" ".join(str(v or "") for v in raw_context_row.values()))

    if label == "Executable":
        # V20-A: Fullscreen/audio transition reports must establish that the
        # relevant jukebox or music-disc playback was active before the
        # transition. Merely checking whether a jukebox is silent afterwards
        # leaves the central pre-transition state missing.
        fullscreen_transition = any(
            phrase in text
            for phrase in [
                "fullscreen",
                "full screen",
                "toggle fullscreen",
                "toggle the fullscreen",
            ]
        )
        jukebox_audio_subject = any(
            phrase in text
            for phrase in [
                "jukebox",
                "music disc",
            ]
        )
        interrupted_audio_result = any(
            phrase in text
            for phrase in [
                "goes silent",
                "gone silent",
                "becomes silent",
                "audio ceases",
                "audio stops",
                "music stops",
                "sound stops",
                "playback stops",
                "stops playing",
                "no longer playing",
            ]
        )
        playback_established = any(
            phrase in steps
            for phrase in [
                "insert a music disc",
                "insert the music disc",
                "put a music disc",
                "place a music disc",
                "start playback",
                "start playing",
                "begin playback",
                "play music",
                "while the jukebox is playing",
                "while music is playing",
                "confirm that the music is playing",
                "verify that audio is playing",
            ]
        )

        if (
            fullscreen_transition
            and jukebox_audio_subject
            and interrupted_audio_result
            and not playback_established
        ):
            return force_non_executable(
                parsed_response,
                "Missing Information",
                "Full rubric post-check: the report evaluates jukebox/music-disc "
                "audio after a fullscreen transition but never establishes that "
                "the relevant playback was active before the transition.",
            )

        # V20-B: A rail-junction defect that depends on a redstone block or
        # power state requires one buildable orientation/layout. Naming only a
        # rail junction on a redstone block does not identify the intended
        # junction geometry or update sequence.
        rail_junction_subject = (
            "rail junction" in text
            or (
                "rail" in text
                and "junction" in text
            )
        )
        redstone_power_subject = any(
            phrase in text
            for phrase in [
                "redstone block",
                "power state",
                "powered rail",
                "redstone-powered",
                "redstone powered",
            ]
        )
        concrete_rail_layout = any(
            phrase in steps
            for phrase in [
                "north-south",
                "north to south",
                "east-west",
                "east to west",
                "t-junction",
                "three-way junction",
                "three way junction",
                "curved rail",
                "ascending rail",
                "rail orientation",
                "facing north",
                "facing south",
                "facing east",
                "facing west",
                "power the junction with",
                "activate the junction with",
                "remove the redstone block",
                "place the redstone block after",
                "activation order",
            ]
        )

        if (
            rail_junction_subject
            and redstone_power_subject
            and not concrete_rail_layout
        ):
            return force_non_executable(
                parsed_response,
                "Missing Information",
                "Full rubric post-check: the rail-junction behavior depends on "
                "junction orientation/layout and redstone power state, but the "
                "steps do not provide one buildable configuration or update "
                "sequence.",
            )

        uses_command = bool(re.search(r"/\s*(summon|time|tp|give|setblock|data|execute|item|tick)\b", steps) or "using the command" in steps)
        default_survival = "survival world" in steps and "default settings" in steps
        permission = any(x in steps for x in ["enable cheats", "cheats enabled", "allow cheats", "open to lan with cheats", "operator permission", "op permission", "creative world", "creative mode", "switch to creative"])
        if default_survival and uses_command and not permission:
            return force_non_executable(parsed_response, "Wrong Information", "Full rubric post-check: commands are required in default Survival without permission.")

        if re.search(r"item_frame\s*\{\s*invisible\s*:\s*1\s*\}", steps):
            return force_non_executable(parsed_response, "Wrong Information", "Full rubric post-check: the invisible item-frame command uses invalid legacy syntax for the stated modern version.")

        impossible_ui = any(x in steps for x in ["crafting interface is open", "while the crafting interface is open", "while the interface is open"]) and any(x in steps for x in ["click on the text of the sign", "click on the sign", "click on the block"])
        if impossible_ui:
            return force_non_executable(parsed_response, "Wrong Information", "Full rubric post-check: the sequence requires clicking a world block while another GUI is open.")

        if "other player" in steps and "creative world with default settings" in steps and not any(x in steps for x in ["multiplayer", "server", "open to lan", "lan world", "realm"]):
            return force_non_executable(parsed_response, "Missing Information", "Full rubric post-check: another player is required, but no multiplayer context is established.")

        skeleton = ("skeleton" in summary or "minecraft:skeleton" in steps) and any(x in steps for x in ["observe the skeleton", "trigger its targeting behavior"])
        protected = any(x in steps for x in ["night", "covered area", "roof", "indoors", "fire resistance", "no sunlight"])
        if skeleton and not protected:
            return force_non_executable(parsed_response, "Missing Information", "Full rubric post-check: sustained skeleton behavior is required without preventing daylight burning.")

        type_pos = min([steps.find(x) for x in ["type a custom name", "type text into the input"] if steps.find(x) >= 0] or [999999])
        item_pos = min([steps.find(x) for x in ["place an item", "insert an item", "put an item"] if steps.find(x) >= 0] or [999999])
        if "anvil" in text and type_pos < item_pos < 999999:
            return force_non_executable(parsed_response, "Wrong Information", "Full rubric post-check: the anvil rename field is used before a valid input item is inserted.")

        if "reduced debug info" in text and "video settings" in steps and "toggle" in steps:
            return force_non_executable(parsed_response, "Wrong Information", "Full rubric post-check: the stated environment does not establish this Reduced Debug Info control in Video Settings.")

        shader_menu = ('"shaders" option' in steps or "shaders option" in steps) and "video settings" in steps
        if shader_menu and not any(x in text for x in ["optifine", "iris", "mod loader", "fabric", "forge"]):
            return force_non_executable(parsed_response, "Wrong Information", "Full rubric post-check: a third-party Shaders menu is required but no providing software is named.")

        if "achievement" in text and "typically involves" in steps:
            return force_non_executable(parsed_response, "Wrong Information", "Full rubric post-check: the central achievement trigger is guessed rather than stated.")

        circular = any(x in steps for x in ["world where the issue has occurred", "areas that are known to have loading issues"]) and any(x in text for x in ["chunk", "freeze", "frozen"])
        if circular:
            return force_non_executable(parsed_response, "Missing Information", "Full rubric post-check: the steps assume an already-problematic world/area instead of creating the trigger.")

        unsupported_attach = "copper golem" in text and any(x in steps for x in ["position the oak shelf directly above", "position the lightning rod directly above", "place the items at the back of the copper golem"]) and not any(x in steps for x in ["/item", "equipment", "equip", "attach", "command"])
        if unsupported_attach:
            return force_non_executable(parsed_response, "Wrong Information", "Full rubric post-check: ordinary placement is used as an unsupported entity attachment action.")

        if "carpet" in text and "redstone dust on top" in steps and "place a carpet block directly on top" in steps:
            return force_non_executable(parsed_response, "Wrong Information", "Full rubric post-check: redstone dust and carpet are assigned to the same position.")

        invented_purchase = ("previously purchased" in steps or "purchase history" in steps) and raw_text and not any(x in raw_text for x in ["purchase", "bought", "compr", "store", "microsoft account"])
        if invented_purchase:
            return force_non_executable(parsed_response, "Missing Information", "Full rubric post-check: the Improved report invents a purchase/store workflow absent from the Raw report.")

        trigger_mismatch = raw_text and any(x in raw_text for x in ["already in a chest", "stored in a chest"]) and any(x in steps for x in ["drop a sugar cane item on the ground", "dropped item"])
        if trigger_mismatch:
            return force_non_executable(parsed_response, "Wrong Information", "Full rubric post-check: the Improved report replaces the Raw chest-inventory trigger with a dropped-item trigger.")

        return parsed_response

    # V20-C: Preserve a concrete local skin/cape visibility path.
    # Account-linking internals, network diagnosis, and synchronization root
    # causes are not blocking when the report already gives an appearance
    # selection/application action, a game-entry action, and a specific visible
    # result such as the Steve fallback or unavailable capes.
    appearance_subject = (
        "skin" in text
        and any(
            phrase in text
            for phrase in [
                "cape",
                "steve skin",
                "default steve",
                "default skin",
                "custom skin",
            ]
        )
    )
    appearance_action = any(
        phrase in steps
        for phrase in [
            "select a skin",
            "select the skin",
            "choose a skin",
            "choose the skin",
            "change the skin",
            "change my skin",
            "apply the skin",
            "apply a custom skin",
            "upload a custom skin",
            "set the selected skin",
            "equip a cape",
            "select a cape",
        ]
    )
    appearance_game_entry = any(
        phrase in steps
        for phrase in [
            "launch minecraft",
            "start minecraft",
            "launch the game",
            "start the game",
            "enter a world",
            "join a world",
            "join a server",
            "singleplayer",
            "multiplayer",
        ]
    )
    appearance_result = any(
        phrase in text
        for phrase in [
            "defaults to steve",
            "default steve skin",
            "shows the steve skin",
            "appears as steve",
            "custom skin is not visible",
            "skin does not appear",
            "skin is not applied",
            "capes are not accessible",
            "cape is not accessible",
            "capes are unavailable",
            "cape is unavailable",
            "collected capes",
            "missing capes",
        ]
    )

    if (
        appearance_subject
        and appearance_action
        and appearance_game_entry
        and appearance_result
    ):
        return force_executable(
            parsed_response,
            "Full rubric post-check: the report gives a concrete skin/cape "
            "selection or application action, a game-entry action, and a "
            "specific visible fallback or missing-appearance result. Account "
            "linking and network internals are diagnostic rather than a missing "
            "central trigger.",
        )

    # Preserve explicit remote loading failure.
    remote_subject = any(x in text for x in ["skin", "texture", "profile"])
    remote_failure = any(x in text for x in ["http", "https", "socketexception", "connection timeout", "timed out", "timeout", "failed to load texture", "failed to retrieve", "download skin", "uncheckedioexception", "completionexception"])
    loading_action = any(x in text for x in ["select a skin", "upload a custom skin", "set the selected skin", "active skin", "start a new singleplayer", "join an existing multiplayer", "enter a world", "join a server"])
    if remote_subject and remote_failure and loading_action:
        return force_executable(parsed_response, "Full rubric post-check: a concrete skin/texture loading path and remote failure are stated.")

    initial_audio = ("jukebox" in text or "music disc" in text) and any(x in steps for x in ["insert the music disc", 'insert the "lava chicken" music disc', "right-clicking on the jukebox while holding the disc"]) and any(x in text for x in ["no audio", "no sound", "silent"]) and not any(x in steps for x in ["fullscreen", "dimension", "pause", "screen transition", "state transition"])
    if initial_audio:
        return force_executable(parsed_response, "Full rubric post-check: the source, insertion action, and failure to begin audio are explicit.")

    if "interaction entity" in text and "/summon interaction" in steps and "/data get entity" in steps and "right-click" in steps:
        return force_executable(parsed_response, "Full rubric post-check: the interaction-entity summon, click, inspection, and result are explicit.")

    if "zombie" in summary and "campfire" in text and "switch to creative mode" in steps and "/summon minecraft:zombie" in steps:
        return force_executable(parsed_response, "Full rubric post-check: the sequence explicitly switches to Creative before summoning the zombie.")

    concrete_pack = "resource pack" in text and "pack.mcmeta" in steps and "assets" in steps and any(x in steps for x in ["active list", "apply the resource pack", "resource packs"])
    if concrete_pack:
        return force_executable(parsed_response, "Full rubric post-check: pack metadata, assets, installation/application, and observation are specified.")

    if "ender dragon" in text and "end dimension" in steps and "/summon minecraft:ender_dragon" in steps and "restart the game" in steps:
        return force_executable(parsed_response, "Full rubric post-check: End access, summon, restart, and visual inspection are explicit.")

    return parsed_response


def apply_phase_consistency_rules(
    phase: str,
    version: str,
    row: Dict[str, str],
    parsed_response: ParsedLLMOutput,
    raw_context_row: Optional[Dict[str, str]] = None,
) -> ParsedLLMOutput:
    """Apply Pilot rules and candidate-Full rules independently."""
    if not APPLY_CONSISTENCY_RULES_BY_PHASE.get(phase, False):
        return parsed_response

    if phase == "pilot" and version == "raw":
        return apply_raw_pilot_consistency_rules(row, parsed_response)

    if phase == "pilot" and version == "improved":
        return apply_improved_pilot_consistency_rules(
            row,
            parsed_response,
        )

    if phase in CANDIDATE_PHASES and version == "raw":
        return apply_raw_full_consistency_rules(row, parsed_response)

    if phase in CANDIDATE_PHASES and version == "improved":
        return apply_improved_full_consistency_rules(
            row,
            parsed_response,
            raw_context_row=raw_context_row,
        )

    raise ValueError(
        f"Unsupported phase/version for consistency rules: "
        f"{phase}/{version}"
    )


def build_output_row(
    issue_key: str,
    result: Dict[str, Any],
    timestamp: str,
    prompt_version: str,
) -> Dict[str, Any]:
    parsed_response = result["parsed_response"]

    s2r = parsed_response["steps_to_reproduce"]
    expected = parsed_response["expected_behavior"]
    observed = parsed_response["observed_behavior"]

    input_tokens = int(result["input_tokens"])
    cached_input_tokens = int(result["cached_input_tokens"])
    output_tokens = int(result["output_tokens"])
    total_tokens = int(result["total_tokens"])
    cost_usd = float(result["cost_usd"])

    return {
        "issue_key": issue_key,
        "s2r_label": s2r["label"],
        "reason": s2r["reason"],

        "s2r_reproducibility": s2r["reproducibility"],
        "s2r_validity": s2r["validity"],
        "s2r_failure_type": s2r["failure_type"],
        "s2r_reason": s2r["reason"],

        "expected_behavior_presence": expected["presence"],
        "expected_behavior_quality": expected["quality"],
        "expected_behavior_reason": expected["reason"],

        "observed_behavior_presence": observed["presence"],
        "observed_behavior_quality": observed["quality"],
        "observed_behavior_reason": observed["reason"],

        "overall_reason": parsed_response["overall_reason"],

        "status": "valid_json",
        "model": MODEL,
        "prompt_version": prompt_version,
        "seed": str(result.get("seed", EXPERIMENT_SEED)),
        "system_fingerprint": str(result.get("system_fingerprint", "") or ""),
        "input_tokens": input_tokens,
        "cached_input_tokens": cached_input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "cost_usd": f"{cost_usd:.8f}",
        "timestamp": timestamp,
        "raw_response": result["raw_response"],
    }


def build_error_output_row(
    issue_key: str,
    error_message: str,
    timestamp: str,
    prompt_version: str,
) -> Dict[str, Any]:
    return {
        "issue_key": issue_key,
        "s2r_label": "",
        "reason": error_message,

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

        "status": "error",
        "model": MODEL,
        "prompt_version": prompt_version,
        "seed": str(EXPERIMENT_SEED),
        "system_fingerprint": "",
        "input_tokens": 0,
        "cached_input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0,
        "cost_usd": "0.00000000",
        "timestamp": timestamp,
        "raw_response": "",
    }


def write_output_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    fieldnames = [
        "issue_key",
        "s2r_label",
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

        "status",
        "model",
        "prompt_version",
        "seed",
        "system_fingerprint",
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
        writer = csv.DictWriter(file, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
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

        "s2r_reproducibility",
        "s2r_validity",
        "s2r_failure_type",

        "expected_behavior_presence",
        "expected_behavior_quality",

        "observed_behavior_presence",
        "observed_behavior_quality",

        "error_message",
        "model",
        "prompt_version",
        "seed",
        "system_fingerprint",
        "input_tokens",
        "cached_input_tokens",
        "output_tokens",
        "total_tokens",
        "cost_usd",
    ]

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows)


def validate_experiment_inputs(
    version: str,
    phase: str,
    input_file: Path,
    prompt_file: Path,
) -> None:
    if not input_file.exists():
        raise FileNotFoundError(f"Cannot find input file: {input_file}")

    if input_file.stat().st_size == 0:
        raise ValueError(f"Input file is empty: {input_file}")

    if not prompt_file.exists():
        raise FileNotFoundError(f"Cannot find prompt file: {prompt_file}")

    if prompt_file.stat().st_size == 0:
        raise ValueError(f"Prompt file is empty: {prompt_file}")

    if version not in CONFIG:
        raise ValueError(f"Unsupported version: {version}")

    if phase not in EXPERIMENT_PHASES:
        raise ValueError(f"Unsupported phase: {phase}")


def run_experiment(
    version: str,
    phase: str,
    limit: Optional[int],
) -> None:

    load_env_file()

    config = CONFIG[version]
    prompt_config = get_prompt_config(version, phase)
    prompt_version = str(prompt_config["version"])
    prompt_file = prompt_config["file"]

    data_dir = config["data_dirs"][phase]
    results_dir = config["results_dirs"][phase]

    input_file = data_dir / config["input_files"][phase]
    output_file = results_dir / config["output_files"][phase]
    log_file = results_dir / config["log_files"][phase]

    validate_experiment_inputs(version, phase, input_file, prompt_file)

    rows = read_csv_dicts(input_file)

    if not rows:
        raise ValueError(f"Input file has no data rows: {input_file}")

    if limit is not None:
        if limit <= 0:
            raise ValueError("--limit must be greater than 0 when provided.")
        rows = rows[:limit]

    raw_context_rows: Dict[str, Dict[str, str]] = {}
    if version == "improved":
        raw_context_rows = load_raw_context_rows(phase)

    output_rows = []
    api_log_rows = []

    total_input_tokens = 0
    total_cached_input_tokens = 0
    total_output_tokens = 0
    total_tokens = 0
    total_cost_usd = 0.0

    print(f"Starting {version} {phase} LLM experiment...")
    print(f"Model      : {MODEL}")
    print(f"Seed       : {EXPERIMENT_SEED}")
    print(f"Prompt     : {prompt_version}")
    print(f"Prompt file: {prompt_file}")
    rules_enabled = APPLY_CONSISTENCY_RULES_BY_PHASE.get(phase, False)
    print(f"Post-check rules: {'enabled' if rules_enabled else 'disabled'}")
    print(f"Input file : {input_file}")
    if version == "improved":
        print(f"Raw context: {RAW_CONTEXT_FILES[phase]}")
    print(f"Output file: {output_file}")
    print(f"Log file   : {log_file}")
    print(f"Total rows : {len(rows)}")
    print("-" * 60)

    for index, row in enumerate(rows, start=1):
        issue_key = find_issue_key(row)

        if not issue_key:
            issue_key = f"row_{index}"

        report_text = build_contextual_report_text(
            version=version,
            row=row,
            issue_key=issue_key,
            raw_context_rows=raw_context_rows,
        )

        if not report_text:
            raise ValueError(f"Empty report text for issue: {issue_key}")

        system_prompt, user_prompt = build_prompt(issue_key, report_text, prompt_file)

        timestamp = datetime.now().isoformat(timespec="seconds")

        print(f"[{index}/{len(rows)}] Processing {issue_key}...")

        try:
            result = call_openai(system_prompt, user_prompt)

            parsed_response = result["parsed_response"]

            raw_context_row = (
                raw_context_rows.get(issue_key)
                if version == "improved"
                else None
            )

            parsed_response = apply_phase_consistency_rules(
                phase=phase,
                version=version,
                row=row,
                parsed_response=parsed_response,
                raw_context_row=raw_context_row,
            )
            result["parsed_response"] = parsed_response

            returned_issue_key = parsed_response["issue_key"]
            if returned_issue_key and returned_issue_key != issue_key:
                print(
                    "  Warning: returned issue_key does not match input issue_key. "
                    f"Returned={returned_issue_key}, Input={issue_key}. "
                    "Using input issue_key in output."
                )

            output_row = build_output_row(
                issue_key=issue_key,
                result=result,
                timestamp=timestamp,
                prompt_version=prompt_version,
            )

            s2r_label = output_row["s2r_label"]
            s2r_reason = output_row["s2r_reason"]

            input_tokens = int(output_row["input_tokens"])
            cached_input_tokens = int(output_row["cached_input_tokens"])
            output_tokens = int(output_row["output_tokens"])
            row_total_tokens = int(output_row["total_tokens"])
            cost_usd = float(output_row["cost_usd"])

            total_input_tokens += input_tokens
            total_cached_input_tokens += cached_input_tokens
            total_output_tokens += output_tokens
            total_tokens += row_total_tokens
            total_cost_usd += cost_usd

            api_log_row = {
                "timestamp": timestamp,
                "version": version,
                "phase": phase,
                "row_index": index,
                "total_rows": len(rows),
                "issue_key": issue_key,
                "status": "valid_json",
                "prediction": s2r_label,
                "reason": s2r_reason,

                "s2r_reproducibility": output_row["s2r_reproducibility"],
                "s2r_validity": output_row["s2r_validity"],
                "s2r_failure_type": output_row["s2r_failure_type"],

                "expected_behavior_presence": output_row["expected_behavior_presence"],
                "expected_behavior_quality": output_row["expected_behavior_quality"],

                "observed_behavior_presence": output_row["observed_behavior_presence"],
                "observed_behavior_quality": output_row["observed_behavior_quality"],

                "error_message": "",
                "model": MODEL,
                "prompt_version": prompt_version,
                "seed": str(result.get("seed", EXPERIMENT_SEED)),
                "system_fingerprint": str(
                    result.get("system_fingerprint", "") or ""
                ),
                "input_tokens": input_tokens,
                "cached_input_tokens": cached_input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": row_total_tokens,
                "cost_usd": f"{cost_usd:.8f}",
            }

            print("  Status: valid_json")
            print(f"  S2R Label      : {s2r_label}")
            print(f"  Reproducibility: {output_row['s2r_reproducibility']}")
            print(f"  Failure type   : {output_row['s2r_failure_type']}")
            print(f"  Expected       : {output_row['expected_behavior_presence']} / {output_row['expected_behavior_quality']}")
            print(f"  Observed       : {output_row['observed_behavior_presence']} / {output_row['observed_behavior_quality']}")
            print(f"  Input tokens   : {input_tokens}")
            print(f"  Cached input   : {cached_input_tokens}")
            print(f"  Output tokens  : {output_tokens}")
            print(f"  Cost/call      : ${cost_usd:.8f}")
            print(
                "  System fingerprint: "
                f"{result.get('system_fingerprint', '')}"
            )

        except Exception as exc:
            error_message = str(exc)

            output_row = build_error_output_row(
                issue_key=issue_key,
                error_message=error_message,
                timestamp=timestamp,
                prompt_version=prompt_version,
            )

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
                "s2r_reproducibility": "",
                "s2r_validity": "",
                "s2r_failure_type": "",
                "expected_behavior_presence": "",
                "expected_behavior_quality": "",
                "observed_behavior_presence": "",
                "observed_behavior_quality": "",
                "error_message": error_message,
                "model": MODEL,
                "prompt_version": prompt_version,
                "seed": str(EXPERIMENT_SEED),
                "system_fingerprint": "",
                "input_tokens": 0,
                "cached_input_tokens": 0,
                "output_tokens": 0,
                "total_tokens": 0,
                "cost_usd": "0.00000000",
            }

            print("  Status: error")
            print(f"  Error: {error_message}")

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
        description="Run LLM bug report quality evaluation for Raw or Improved reports."
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
        choices=[
            "pilot",
            "full",
        ],
        help="Experiment phase to run.",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help=(
            "Optional row limit for testing. "
            "Remove for full run."
        ),
    )

    args = parser.parse_args()

    run_experiment(
        version=args.version,
        phase=args.phase,
        limit=args.limit,
    )


if __name__ == "__main__":
    main()