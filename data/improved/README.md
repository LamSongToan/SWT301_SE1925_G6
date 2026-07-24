# Data — Improved

This folder holds the **Improved** bug reports: the same 139 Mojira issues
after the ImproBR pipeline used an LLM to rewrite them (clarifying or adding
Steps to Reproduce, Observed Behavior, Expected Behavior, and Environment).

Improved is one of the study's two co-equal datasets (the other is
`data/raw/`). The identical evaluation pipeline is run on both, because the
research question asks whether the LLM stays close to human judgment on the
AI-improved reports as well as on the raw ones.

| File | Cases | Description |
| --- | --- | --- |
| `improved dataset/` | 139 | Source JSON reports |
| `pilot_sample_improved.csv` | 26 | Pilot report text |
| `pilot_ground_truth_improved.csv` | 26 | Pilot consensus labels |
| `pilot_annotation_improved_author1.csv` | 26 | Pilot annotation, first annotator |
| `pilot_annotation_improved_author2.csv` | 26 | Pilot annotation, second annotator |
| `full_sample_improved.csv` | 139 | Full report text sent to the model |
| `full_ground_truth_improved.csv` | 139 | Full consensus labels |

## Two phases, matching the proposal

The Improved dataset follows the same Pilot → Full pipeline as Raw. See
`results/improved/README.md` for the pilot numbers and `results/full/` for the
full-phase results.

Join on `issue_key`, which is `BUG-ID` with the trailing ` Improved` suffix
removed.

See `../README.md` for the label definitions and how labels become a 1-5
reproducibility score.
