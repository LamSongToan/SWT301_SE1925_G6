# Data

This folder holds everything the experiment uses as **input**. Nothing here
is produced by the LLM.

## What study this data supports

The project follows the proposal in `proposal.md`: we test how closely
GPT-4o mini agrees with human reproducibility judgment (a 1-5 score), measured
with Cohen's Kappa against a threshold of ≥ 0.70.

The study uses **two datasets, treated equally**:

- **Raw** — the 139 original Mojira (Minecraft) bug reports as submitted.
- **Improved** — the *same* 139 reports after the ImproBR pipeline used an LLM
  to rewrite them (clarifying or adding Steps to Reproduce, Observed Behavior,
  Expected Behavior, and Environment).

We run the identical evaluation on both, because the research question asks
whether the LLM stays close to human judgment on **both** the raw reports and
the AI-improved reports. Raw and Improved are two co-equal conditions, not a
primary dataset plus a supplement.

## Origin

All reports and annotations come from the ImproBR replication package
(Akyol et al., 2026, arXiv:2604.26142). Each Raw report and each Improved
report was independently annotated by two human reviewers using the same
rubric.

## Layout

| Path | Contents |
| --- | --- |
| `annotations/` | Author 1 and Author 2 responses, the consensus labels, and the rubric |
| `raw/` | Raw source reports plus Raw pilot and full datasets |
| `improved/` | Improved source reports plus Improved pilot and full datasets |

### annotations/

| File | Description |
| --- | --- |
| `Author 1 Responses.csv` | Independent annotation, first annotator |
| `Author 2 Responses.csv` | Independent annotation, second annotator |
| `Final Results.csv` | Consensus labels used as ground truth |
| `evaluation_metrics.yaml` | Rubric defining every label |

Each row covers one report in one form; the `BUG-ID` column carries the form
as a suffix, for example `MC-300562 Raw` or `MC-300562 Improved`. There are
278 annotated rows in total (139 issues x 2 forms).

## Turning labels into a reproducibility score

Both datasets are scored on the same 1-5 reproducibility scale, computed from
the structured labels (S2R, OB, EB) with one fixed, deterministic function
(see `proposal.md`, Section 5.3, and the analysis notebooks in `results/`).
The same function is applied to human labels and to LLM output, so any
difference in score reflects a difference in judgment, not a difference in
scoring rules.

## Note on empty cells

`Final Results.csv` ends with blank filler rows, and quality columns are left
empty where a section is absent. Scripts must therefore drop rows without a
`BUG-ID` and treat an empty quality cell as "not applicable" rather than as a
distinct label. Comparing an empty cell against the literal string
`Not Applicable` would otherwise be counted as a disagreement by mistake.
