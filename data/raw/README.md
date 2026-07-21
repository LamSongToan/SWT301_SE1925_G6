# Data — Raw

Raw-form source reports and the datasets derived from them. One of the two
conditions in the study; `data/improved/` mirrors this directory.

| File | Cases | Description |
| --- | --- | --- |
| `raw dataset/` | 139 | Source JSON reports |
| `pilot_sample_raw.csv` | 26 | Pilot report text |
| `pilot_ground_truth_raw.csv` | 26 | Pilot consensus labels |
| `pilot_annotation_raw_author1.csv` | 26 | Pilot annotation, first annotator |
| `pilot_annotation_raw_author2.csv` | 26 | Pilot annotation, second annotator |
| `full_sample_raw.csv` | 139 | Full report text sent to the model |
| `full_ground_truth_raw.csv` | 139 | Full consensus labels |

The `*_sample_*` files hold the text given to the model. The
`*_ground_truth_*` files hold the labels the model is scored against; they are
never shown to the model.

Join on `issue_key`, which is `BUG-ID` with the trailing ` Raw` suffix
removed.

See `../README.md` for the label definitions and class balance.
