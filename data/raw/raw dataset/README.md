# Raw source reports

Original Mojira (Minecraft) bug reports as submitted by reporters, before any
rewriting. One JSON file per issue, named by its Mojira key, for example
`MC-298921.json`.

## Origin

Taken from the ImproBR replication package (Akyol et al., 2026,
arXiv:2604.26142), which selected these 139 issues from the public Mojira issue
tracker. Licensing follows that package; the underlying reports are user
submissions to Mojang's public tracker.

## Fields

| Field | Description |
| --- | --- |
| `key` | Mojira issue identifier, joins to every other file in the repository |
| `summary` | Issue title |
| `description` | Full report body, including any steps to reproduce |
| `created_date`, `updated_date` | Timestamps from the tracker |
| `status`, `resolution`, `resolution_date` | Tracker workflow state |
| `affected_versions`, `fix_versions` | Minecraft versions |
| `confirmation_status` | Mojira triage state |
| `category` | Tracker category |

## Use

`scripts/03_create_full_samples.py` reads these files and writes
`../full_sample_raw.csv`, which is the text actually sent to the model. Only
`summary` and `description` reach the model; status, resolution, and version
metadata are deliberately withheld so the evaluator cannot infer the label from
triage outcomes.

The directory holds 139 reports plus this file.
