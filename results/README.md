# Results

This folder stores every output produced while running the experiment
described in `proposal.md`: how closely does GPT-4o mini agree with human
reproducibility judgment (a 1-5 score), measured with Cohen's Kappa against a
threshold of ≥ 0.70?

The study runs the **same pipeline on two co-equal datasets** — **Raw** (the
original reports) and **Improved** (the same reports after the ImproBR LLM
rewrote them) — following the proposal's two-phase design: a Pilot phase to
check the setup, then a Full phase on all 139 reports.

## Folder layout

| Folder / file | What it holds |
| --- | --- |
| `raw/` | Pilot-phase outputs on the Raw dataset |
| `improved/` | Pilot-phase outputs on the Improved dataset |
| `full/` | Full-phase outputs (139 reports) for both Raw and Improved, plus the analysis notebooks |

## The two phases

### Phase 0 — Pilot (26 reports)

Before scoring all 139 reports, the proposal requires two checks on a 26-report
pilot sample, run independently for each dataset:

1. **Are the two human annotators consistent with each other?**
   Cohen's Kappa between Author 1 and Author 2, using the same 1-5 scoring
   function used everywhere in the study.
   - Raw: κ = 0.7647 (passes the ≥ 0.60 check)
   - Improved: κ = 0.7524 (passes the ≥ 0.60 check)
2. **Does the model's zero-shot prompt already agree well enough with humans?**
   Cohen's Kappa between the LLM's pilot output and the pilot ground truth.
   - Raw: κ = 0.5667 (passes the ≥ 0.50 check → keep zero-shot)
   - Improved: κ = 0.5761 (passes the ≥ 0.50 check → keep zero-shot)

Because both checks passed on both datasets, the proposal's few-shot fallback
was not needed, and each Full phase used the same fixed zero-shot prompt as its
pilot.

### Phase 1 — Full (139 reports)

Every report is scored once by the model, using the prompt confirmed in the
Pilot phase. Cohen's Kappa is then computed between the LLM's 1-5 score and
the human ground-truth score, for each dataset.

| Dataset | Composite Kappa (LLM vs. human) | Human-human Kappa (κ_control) | Passes 0.70 threshold? |
| --- | --- | --- | --- |
| **Raw** | **0.578** (moderate) | 0.674 | No — below threshold |
| **Improved** | **0.335** (fair) | 0.556 | No |

The headline finding is the **gap between the two**: the LLM stays reasonably
close to human judgment on Raw reports, but agreement drops sharply on the
AI-improved reports, where the model tends to rate the polished text as
fully reproducible far more often than the human annotators do. Both datasets
also break down by dimension (Steps to Reproduce, Observed Behavior, Expected
Behavior); see the paper (`paper/sections/04_results.tex`) for the full
breakdown, the bias tests, and the qualitative disagreement analysis.

## How the numbers are computed

The official metric computation lives in the analysis notebooks
(`full_analysis_raw.ipynb`, `full_analysis_improved.ipynb`,
`pilot_analysis_raw.ipynb`, `pilot_analysis_improved.ipynb`). All four
notebooks use the exact same steps — they only point at a different input
file (Raw vs. Improved, Pilot vs. Full):

1. Load the ground-truth CSV and the LLM output CSV, and merge them by
   `issue_key`.
2. Apply the deterministic scoring function from `proposal.md` (Section 5.3)
   to both the ground-truth labels and the LLM labels, producing a 1-5 score
   for each report.
3. Compute Cohen's Kappa between the two sets of scores. This is the study's
   primary metric.
4. Also report per-label accuracy/precision/recall/F1 for each of the six
   underlying annotation fields (S2R, S2R Irrep, OB Category, OB Label, EB
   Category, EB Label), as supporting detail.

`scripts/compute_metric.py` is a separate, simpler helper script. It only
checks one field (the S2R Executable / Non-Executable label) and is not the
official metric for this study; treat its output as a quick sanity check.

## Common result files

| File pattern | Description |
| --- | --- |
| `*_api_log_*.csv` | API call log: status, token usage, cost |
| `*_llm_output_*.csv` | Structured LLM predictions for each report |
| `summary_*.csv` | Aggregate metrics written by `compute_metric.py` (S2R-only sanity check) |
| `mismatch_analysis_*.csv` | Reports where the LLM's S2R label differs from ground truth |
| `*_analysis.ipynb` | The official analysis notebooks described above |

> Note: the `*_llm_output_*.csv` and `*_api_log_*.csv` files under `full/`
> record the actual run and still carry the old full-phase prompt-version
> labels in their `prompt_version` column. See `../V11_REMOVAL_LOG.md`.
