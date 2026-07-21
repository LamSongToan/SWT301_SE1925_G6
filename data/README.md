# Data

Source reports, human annotations, and the derived datasets used in the
experiment. Everything here is input; nothing in this directory is produced by
the LLM.

## Origin

All reports and annotations come from the ImproBR replication package
(Akyol et al., 2026, arXiv:2604.26142). That package covers 139 Mojira
(Minecraft) bug reports in two forms:

- **Raw** — the original text submitted by the reporter.
- **Improved** — the same report after the ImproBR pipeline rewrote it.

Both forms are studied here as two separate conditions on the same 139 issues.

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

Each row covers one report in one form; the `BUG-ID` column carries the form as
a suffix, for example `MC-300562 Raw`. There are 278 annotated rows in total
(139 issues x 2 forms).

### raw/ and improved/

The two directories mirror each other.

| File | Cases | Description |
| --- | --- | --- |
| `<form> dataset/` | 139 | Source JSON reports |
| `pilot_sample_<form>.csv` | 26 | Pilot report text |
| `pilot_ground_truth_<form>.csv` | 26 | Pilot consensus labels |
| `pilot_annotation_<form>_author1.csv` | 26 | Pilot annotation, first annotator |
| `pilot_annotation_<form>_author2.csv` | 26 | Pilot annotation, second annotator |
| `full_sample_<form>.csv` | 139 | Full report text sent to the model |
| `full_ground_truth_<form>.csv` | 139 | Full consensus labels |

## Labels

The primary label is `S2R Label`, with two values:

- **Executable** — the steps lead deterministically to the reported behavior.
- **Non-Executable** — at least one blocking problem is present, such as
  missing, wrong, or ambiguous information.

Class balance differs sharply between the two forms, which is why agreement is
reported with chance-corrected Cohen's kappa rather than accuracy:

| Form | Executable | Non-Executable |
| --- | --- | --- |
| Raw | 40 (28.8%) | 99 (71.2%) |
| Improved | 94 (67.6%) | 45 (32.4%) |

The annotation files also carry `OB` and `EB` columns describing Observed and
Expected Behavior. The study reports S2R as the primary outcome; the other
dimensions are secondary.

## Note on empty cells

`Final Results.csv` ends with blank filler rows, and quality columns are left
empty where a section is absent. Scripts must therefore drop rows without a
`BUG-ID` and treat an empty quality cell as "not applicable" rather than as a
distinct label. Comparing an empty cell against the model's literal
`Not Applicable` string will otherwise count as a disagreement.
