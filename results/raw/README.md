# Pilot Results — Raw

This folder holds the Pilot-phase output for the Raw dataset (26 reports),
the calibration step required before the Full run, as described in
`proposal.md` Section 5.1.

## What the Pilot phase checks

| Check | Metric | Result | Pass condition | Passed? |
| --- | --- | --- | --- | --- |
| Are the two human annotators consistent? | Cohen's Kappa, Author 1 vs. Author 2 | κ = 0.7647 | κ ≥ 0.60 | Yes |
| Does the zero-shot prompt already agree with humans? | Cohen's Kappa, LLM vs. pilot ground truth | κ = 0.5667 | κ ≥ 0.50 | Yes |

Both checks passed, so the proposal's few-shot fallback was not triggered.
The Full phase (see `../full/`) used the same fixed zero-shot prompt on all
139 Raw reports.

Both Kappa values are computed with the same 1-5 deterministic scoring
function used everywhere in this study (`proposal.md`, Section 5.3), inside
`pilot_analysis_raw.ipynb`.

## Files in this folder

| File | Description |
| --- | --- |
| `pilot_api_log_raw.csv` | API call log for the Pilot run |
| `pilot_llm_output_raw.csv` | LLM predictions for the 26 Pilot reports |
| `pilot_analysis_raw.ipynb` | Notebook that computes the Pilot Kappa values above |
| `summary_raw.csv` | Output of `scripts/compute_metric.py` — a simpler, S2R-only sanity check, not the official Pilot metric |
