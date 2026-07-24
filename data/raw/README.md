# Data — Raw

This folder holds the **Raw** bug reports: the original text submitted to
Mojira, before any rewriting. Raw is one of the study's two co-equal datasets
(the other is `data/improved/`); the same evaluation pipeline is run on both.

| File | Cases | Description |
| --- | --- | --- |
| `raw dataset/` | 139 | Source JSON reports (one file per issue) |
| `pilot_sample_raw.csv` | 26 | Pilot report text sent to the model |
| `pilot_ground_truth_raw.csv` | 26 | Pilot consensus labels |
| `pilot_annotation_raw_author1.csv` | 26 | Pilot annotation, first annotator |
| `pilot_annotation_raw_author2.csv` | 26 | Pilot annotation, second annotator |
| `full_sample_raw.csv` | 139 | Full report text sent to the model |
| `full_ground_truth_raw.csv` | 139 | Full consensus labels |

## Two phases, matching the proposal

1. **Pilot phase** (26 reports): used to check two things before the full run.
   - Are the human annotations consistent enough to trust as ground truth?
   - Does the model's zero-shot prompt already agree well enough with humans,
     or does the proposal's few-shot fallback need to be triggered?
   See `results/raw/README.md` for the pilot numbers.
2. **Full phase** (139 reports): the model scores every report once, with the
   prompt fixed after the pilot check.

The `*_sample_*` files hold the text given to the model. The
`*_ground_truth_*` files hold the labels the model is scored against; they
are never shown to the model.

Join on `issue_key`, which is `BUG-ID` with the trailing ` Raw` suffix
removed.

See `../README.md` for how labels are turned into a 1-5 reproducibility score.
