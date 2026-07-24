  # Can an LLM Judge Bug-Report Reproducibility? Evaluating GPT-4o mini on Raw and AI-Improved Mojira Reports

**Course project — SWT301, Group SE1925_G6 (RT-SWT-004)**

**Repository Link:** https://github.com/LamSongToan/SWT301_SE1925_G6

This repository contains the full replication package for a study that asks a
single question: **can a large language model, used as an automated evaluator,
agree with human developers on whether a bug report is reproducible?** We
measure that agreement with Cohen's Kappa against a pre-registered threshold of
**κ ≥ 0.70**.

The twist is that we run the *same* evaluation on two co-equal versions of the
same 139 Minecraft/Mojira bug reports: the original **Raw** reports, and
**Improved** versions that another LLM pipeline (ImproBR) has already rewritten
to look more complete. This lets us test not only whether the model tracks human
judgment on ordinary reports, but whether that agreement survives once the text
has been polished by AI.

## Effort contribution:

| StudentID | Name | Effort (%)
|---------|------|----------|
| SE160995 | Tống Gia Huy | 19% | 
| SE193500 | Trần Thái Dương | 19% | 
| SE203653 | Nguyễn Hồng Quân | 21% | 
| SE203692 | Nguyễn Thành Lộc | 20% | 
| SE200458 | Lâm Song Toàn | 21% | 

---

## Headline result

The model (GPT-4o mini, fixed snapshot `gpt-4o-mini-2024-07-18`, temperature 0)
does **not** reach the κ ≥ 0.70 bar on either form, and it gets markedly worse on
the AI-improved reports.

| Dataset | Composite κ (LLM vs. human) | Human–human κ (ceiling) | Meets κ ≥ 0.70? |
| --- | --- | --- | --- |
| **Raw** | **0.578** (moderate) | 0.674 | No |
| **Improved** | **0.335** (fair) | 0.556 | No |

On the Improved form the model develops a strong optimistic bias: it rates 111
of 139 reports as reproducible against the humans' 94, and scores *higher* than
the annotator in 47 of 52 disagreements. Agreement stays highest on the
structurally checkable **Steps to Reproduce** dimension and collapses on the
free-text **Observed / Expected Behavior** dimensions — exactly where the ImproBR
rewrite makes the text read as complete.

> **Note on two metrics.** The table above is the study's *official* composite
> 1–5 score, computed in the analysis notebooks under `results/`. A separate
> helper, `scripts/compute_metric.py`, only checks the single S2R label and is a
> quick sanity check (it reports κ = 0.336 Raw / 0.059 Improved on that one
> field). Do not confuse the two.

---

## Research questions

- **RQ1 / SQ1 — Overall agreement.** How well does the LLM's reproducibility
  score agree with human ground truth (Cohen's Kappa)?
- **SQ2 — Per-dimension agreement.** Does agreement differ across Steps to
  Reproduce, Observed Behavior, and Expected Behavior?
- **SQ3 — Disagreement analysis.** What features of a report cause systematic
  disagreement between the LLM and the annotators?

The full protocol, PICO framing, and literature gap analysis live in
`SLR/proposal.md` and the `SLR/` folder.

---

## Repository layout

```
.
├── SLR/            Systematic literature review: proposal, search log,
│                   screening CSVs, evidence table, gap analysis, source PDFs
├── data/           All experiment INPUT (nothing here is produced by the LLM)
│   ├── annotations/    Author 1 / Author 2 responses, consensus labels, rubric
│   ├── raw/            Raw source reports + pilot/full samples & ground truth
│   └── improved/       Improved source reports + pilot/full samples & ground truth
├── scripts/        Data preparation + experiment execution (numbered 00–06)
│   └── prompts/        Pilot and full prompt templates (Raw / Improved)
├── results/        All experiment OUTPUT: LLM predictions, API logs, summaries,
│                   and the official analysis notebooks
├── paper/          LaTeX manuscript (sections, figures, refs) + compiled PDF
├── presentation/   Proposal and final slide decks (pptx + pdf)
├── Notes.md        Bilingual (EN/VI) running project log and status
└── LICENSE         MIT
```

Every major folder has its own README (`data/README.md`, `scripts/README.md`,
`results/README.md`, and per-dataset READMEs) with more detail than this summary.

---

## Dataset

- **Source:** ImproBR Replication Package (Akyol et al., 2026), hosted on
  [Figshare](https://figshare.com/articles/software/ImproBR_Replication_Package/30086083).
- **Domain:** Mojira — the official Minecraft issue tracker.
- **Size:** 139 bug reports, each present in two forms (Raw and Improved) =
  278 annotated instances.
- **Annotation:** every instance was labelled independently by two human
  reviewers along three dimensions — Steps to Reproduce (S2R), Observed
  Behavior (OB), Expected Behavior (EB) — using the rubric in
  `data/annotations/evaluation_metrics.yaml`. Consensus labels in
  `Final Results.csv` are the ground truth.

Both human labels and LLM output are converted to a common **1–5 reproducibility
score** by one fixed, deterministic scoring function, so any score difference
reflects a difference in judgment rather than in scoring rules.

> Please verify the dataset's own license on the original Figshare package
> before redistributing the report contents.

---

## Reproducing the experiment

### 1. Requirements

- Python 3.10+
- Packages: `openai`, `scikit-learn`, `pandas`, `numpy`, `matplotlib`
  (Jupyter to open the analysis notebooks)

```bash
python -m venv .venv
# Windows:      .\.venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate
pip install openai scikit-learn pandas numpy matplotlib jupyter
```

### 2. API key

The scripts read the key from the environment — never commit it.

```bash
# Windows
set OPENAI_API_KEY=your_key_here
# macOS / Linux
export OPENAI_API_KEY=your_key_here
```

### 3. Run order

Run everything from the repository root so relative paths resolve. Steps 0–3
rebuild the datasets from the annotation files and are **already committed**;
re-run them only if you want to regenerate the inputs.

| Step | Command | Purpose |
| --- | --- | --- |
| 0 | `python scripts/00_generate_pilot.py` | Draw the 26-report pilot sample + ground truth |
| 1 | `python scripts/01_create_full_ground_truth_improved.py` | Build the 139-report Improved ground truth |
| 2 | `python scripts/02_create_full_ground_truth_raw.py` | Build the 139-report Raw ground truth |
| 3 | `python scripts/03_create_full_samples.py` | Build the report text sent to the model (both datasets) |
| 4 | `python scripts/test_api.py --version raw` | One-report connectivity / JSON-parse check |
| 5 | `python scripts/run_experiment.py --version <raw\|improved> --phase <pilot\|full>` | Score a dataset; writes LLM output + API log |
| 6 | `python scripts/compute_metric.py --version <raw\|improved> --phase <pilot\|full>` | Fast S2R-only sanity check (not the official metric) |

Example full run for both datasets:

```bash
python scripts/run_experiment.py  --version raw      --phase full
python scripts/run_experiment.py  --version improved --phase full
```

`run_experiment.py` also accepts `--limit N` to score only the first N reports
while testing.

### 4. Official metric & figures

The study's real numbers (composite 1–5 Cohen's Kappa, per-dimension κ, bias
tests) come from the analysis notebooks, not from `compute_metric.py`:

- `results/full/full_analysis_raw.ipynb`
- `results/full/full_analysis_improved.ipynb`
- `results/*/pilot_analysis_*.ipynb` (pilot gating checks)

All four notebooks share the same steps and differ only in which input file they
load: merge ground-truth and LLM output on `issue_key`, apply the deterministic
1–5 scoring function, then compute Cohen's Kappa. Figures in `paper/figures/`
are regenerated with `python scripts/make_figures.py`.

---

## Two-phase design (pilot gating)

Before the full 139-report run, a 26-report **pilot** must clear two checks per
dataset (per `proposal.md` §5.1):

1. Human–human κ ≥ 0.60 — annotations are consistent enough to trust.
   *(Raw 0.7647, Improved 0.7524 — both pass.)*
2. LLM-vs-human κ ≥ 0.50 — the zero-shot prompt is good enough, otherwise a
   few-shot fallback is triggered. *(Raw 0.5667, Improved 0.5761 — both pass.)*

Because both checks passed on both datasets, each full run used the same fixed
zero-shot prompt as its pilot (Raw prompt V10, Improved prompt V18). The prompt
was **not** revised after inspecting results.

---

## Conventions & gotchas

- Read/write CSV as `utf-8-sig`; the annotation files carry a BOM.
- Join on `issue_key`, i.e. `BUG-ID` with the trailing ` Raw` / ` Improved`
  suffix removed.
- Treat an empty quality cell in the ground truth as equivalent to the model's
  `Not Applicable`; otherwise every absent section is miscounted as a
  disagreement.
- **Never** feed ground-truth files to the LLM — use the `*_sample_*` files as
  input.
- Do not change the pre-registered statistical test after seeing results.

---

## Team

Group SE1925_G6: Lâm Song Toàn (SE200458), Nguyễn Thành Lộc (SE203692),
Nguyễn Hồng Quân (SE203653), Tống Gia Huy (SE160995), Trần Thái Dương (SE193500).

## License

Code is released under the MIT License (see `LICENSE`). The bug-report data is
governed by the original ImproBR / Figshare package license — verify it before
redistribution.

## Citing the data source

> Akyol et al. (2026). *ImproBR Replication Package.* Figshare.
> https://figshare.com/articles/software/ImproBR_Replication_Package/30086083
