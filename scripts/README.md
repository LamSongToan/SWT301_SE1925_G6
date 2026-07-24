# Scripts

Data preparation and experiment execution for the study described in
`proposal.md`. Run everything from the repository root so that relative
paths resolve.

## Order of execution

| Step | Script | Purpose |
| --- | --- | --- |
| 0 | `00_generate_pilot.py` | Draws the 26-report pilot sample and its ground truth |
| 1 | `01_create_full_ground_truth_improved.py` | Builds the 139-report Improved ground truth (supplementary) |
| 2 | `02_create_full_ground_truth_raw.py` | Builds the 139-report Raw ground truth (official) |
| 3 | `03_create_full_samples.py` | Builds the 139-report text sent to the model, for both datasets |
| 4 | `test_api.py` | Sends one report to check API connectivity and JSON parsing |
| 5 | `run_experiment.py` | Runs the model over a dataset/phase and writes LLM output plus an API log |
| 6 | `compute_metric.py` | Quick sanity check: accuracy and Cohen's Kappa on the S2R label only (see note below) |

Steps 0 to 3 are already committed. Re-run them only to rebuild the datasets
from the annotation files.

## Where the official metric is computed

`compute_metric.py` (step 6) only checks one field — S2R Executable vs.
Non-Executable — and is a fast sanity check, not the study's official result.

The **official metric**, matching `proposal.md` Section 5.3–6, is computed in
the analysis notebooks under `results/`:

- `results/raw/pilot_analysis_raw.ipynb`, `results/improved/pilot_analysis_improved.ipynb`
  — Pilot-phase Kappa checks (human-human and LLM-human).
- `results/full/full_analysis_raw.ipynb`, `results/full/full_analysis_improved.ipynb`
  — Full-phase Kappa on all 139 reports.

All four notebooks follow the same steps and only differ in which input file
they load (Raw vs. Improved, Pilot vs. Full):

1. Merge the ground-truth CSV and the LLM output CSV on `issue_key`.
2. Apply the deterministic 1-5 scoring function from the proposal to both
   the ground-truth labels and the LLM labels.
3. Compute Cohen's Kappa between the two resulting 1-5 scores.

## Pilot gating logic (proposal Section 5.1)

Before running the Full phase, the Pilot phase must pass two checks, run
independently for each of the two datasets (Raw and Improved):

1. κ between the two human annotators ≥ 0.60 (annotations are consistent
   enough to trust as ground truth).
2. κ between the LLM's pilot output and the pilot ground truth ≥ 0.50 (the
   zero-shot prompt is good enough; otherwise switch to the few-shot
   fallback prompt for the Full run).

Both checks passed for both datasets — Raw (κ = 0.7647 and κ = 0.5667) and
Improved (κ = 0.7524 and κ = 0.5761) — so each Full run used the same fixed
zero-shot pilot prompt for all 139 reports (raw: V10, improved: V18).

## prompts/

| Path | Used for |
| --- | --- |
| `prompts/pilot/` | Prompt version used in the 26-report pilot |
| `prompts/full/` | Prompt version used in the 139-report full run (same prompt as the pilot, per the proposal's fixed-prompt design) |

Each prompt states the rubric, supplies the report, and requires a JSON
reply. The version string is recorded in every output row.

## API key

`run_experiment.py` and `test_api.py` read the key from the environment.
Never put it in a file inside the repository.

```bash
# Windows
set OPENAI_API_KEY=your_key_here
# macOS / Linux
export OPENAI_API_KEY=your_key_here
```

## Conventions

- Read and write CSV as `utf-8-sig`; the annotation files carry a BOM.
- Join on `issue_key` after stripping the ` Raw` or ` Improved` suffix from
  `BUG-ID`.
- Treat an empty quality cell in the ground truth as equivalent to the
  model's `Not Applicable`, otherwise every absent section counts as a
  disagreement.
