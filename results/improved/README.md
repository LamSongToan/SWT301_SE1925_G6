# Pilot Results — Improved

This folder holds the Pilot-phase output for the **Improved** dataset (26
reports). Improved is one of the study's two co-equal datasets (see
`data/improved/README.md`); it runs through the same Pilot → Full pipeline as
Raw.

## Pilot checks (same method as the Raw dataset)

| Check | Metric | Result | Pass condition | Passed? |
| --- | --- | --- | --- | --- |
| Human annotator consistency | Cohen's Kappa, Author 1 vs. Author 2 | κ = 0.7524 | κ ≥ 0.60 | Yes |
| Zero-shot prompt vs. pilot ground truth | Cohen's Kappa, LLM vs. pilot ground truth | κ = 0.5761 | κ ≥ 0.50 | Yes |

Both checks passed, so the proposal's few-shot fallback was not triggered.
The Full phase (see `../full/`) used the same fixed zero-shot prompt on all
139 Improved reports.

Both Kappa values are computed with the same 1-5 deterministic scoring
function used everywhere in this study (`proposal.md`, Section 5.3), inside
`pilot_analysis_improved.ipynb`.

## Files in this folder

| File | Description |
| --- | --- |
| `pilot_api_log_improved.csv` | API call log for the Pilot run |
| `pilot_llm_output_improved.csv` | LLM predictions for the 26 Pilot reports |
| `pilot_analysis_improved.ipynb` | Notebook that computes the Pilot Kappa values above |
| `summary_improved.csv` | Output of `scripts/compute_metric.py` — a simpler, S2R-only sanity check, not the official Pilot metric |
