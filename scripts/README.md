# Scripts

Data preparation, experiment execution, and metric computation. Run everything
from the repository root so that relative paths resolve.

## Order of execution

| Step | Script | Purpose |
| --- | --- | --- |
| 0 | `00_generate_pilot.py` | Draws the 26-case pilot sample and its ground truth |
| 1 | `01_create_full_ground_truth_improved.py` | Builds the 139-case Improved ground truth |
| 2 | `02_create_full_ground_truth_raw.py` | Builds the 139-case Raw ground truth |
| 3 | `03_create_full_samples.py` | Builds the 139-case report text for both conditions |
| 4 | `test_api.py` | Sends one report to check connectivity and JSON parsing |
| 5 | `run_experiment.py` | Runs the model over a dataset and writes LLM output plus an API log |
| 6 | `compute_metric.py` | Computes accuracy, Cohen's kappa, the confusion matrix, and mismatches |

Steps 0 to 3 are already committed. Re-run them only to rebuild the datasets
from the annotation files.

## prompts/

| Path | Used for |
| --- | --- |
| `prompts/pilot/` | Prompt versions used in the 26-case pilot |
| `prompts/full/` | Prompt versions used in the 139-case full run |

Each prompt states the rubric, supplies the report, and requires a JSON reply.
The version string is recorded in every output row.

## API key

`run_experiment.py` and `test_api.py` read the key from the environment. Never
put it in a file inside the repository.

```bash
# Windows
set OPENAI_API_KEY=your_key_here
# macOS / Linux
export OPENAI_API_KEY=your_key_here
```

## What compute_metric.py checks

Beyond computing the metrics, it refuses to score silently broken input. It
reports duplicate issue keys, predictions with no matching ground truth, ground
truth rows with no prediction, and labels outside the allowed vocabulary. If any
of these appear, fix the input rather than the metric.

## Conventions

- Read and write CSV as `utf-8-sig`; the annotation files carry a BOM.
- Join on `issue_key` after stripping the ` Raw` or ` Improved` suffix from
  `BUG-ID`.
- Treat an empty quality cell in the ground truth as equivalent to the model's
  `Not Applicable`, otherwise every absent section counts as a disagreement.
