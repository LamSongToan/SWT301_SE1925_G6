# Data — Improved

Improved-form source reports and the datasets derived from them. One of the two
conditions in the study; `data/raw/` mirrors this directory.

| File | Cases | Description |
| --- | --- | --- |
| `improved dataset/` | 139 | Source JSON reports |
| `pilot_sample_improved.csv` | 26 | Pilot report text |
| `pilot_ground_truth_improved.csv` | 26 | Pilot consensus labels |
| `pilot_annotation_improved_author1.csv` | 26 | Pilot annotation, first annotator |
| `pilot_annotation_improved_author2.csv` | 26 | Pilot annotation, second annotator |
| `full_sample_improved.csv` | 139 | Full report text sent to the model |
| `full_ground_truth_improved.csv` | 139 | Full consensus labels |

The `*_sample_*` files hold the text given to the model. The
`*_ground_truth_*` files hold the labels the model is scored against; they are
never shown to the model.

Join on `issue_key`, which is `BUG-ID` with the trailing ` Improved` suffix
removed.

See `../README.md` for the label definitions and class balance.
