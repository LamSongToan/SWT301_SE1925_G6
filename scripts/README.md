# Scripts Workflow / Quy trình thư mục Scripts

## English

### Purpose — English

The `Scripts` directory prepares Pilot and Full data, runs the LLM experiments,
computes metrics, compares Raw and Improved results, and supports mismatch
analysis.

### Main scripts — English

| Script | Function |
| --- | --- |
| `generate_pilot.py` | Creates Pilot samples, Ground Truth, and annotation files. |
| `kappa_pilot.py` | Computes Pilot inter-annotator Cohen's Kappa. |
| `Raw/create_full_ground_truth_raw.py` | Creates the 139-case Raw Full Ground Truth. |
| `Improved/create_full_ground_truth_improved.py` | Creates the 139-case Improved Full Ground Truth. |
| `create_full_samples.py` | Creates the 139-case Raw and Improved Full samples. |
| `create_development_holdout_split.py` | Creates the 26/75/38 Pilot–Development–Holdout split. |
| `fix_full_ground_truth_headers.py` | Repairs duplicate Ground Truth headers when needed. |
| `test_api.py` | Tests one non-Holdout case without creating CSV output. |
| `run_experiment.py` | Runs Pilot, Development, Pilot Validation, or Holdout. |
| `compute_metric.py` | Computes Accuracy, Cohen's Kappa, confusion matrix, mismatch, tokens, and cost. |
| `compare_raw_improved.py` | Compares Raw and Improved summaries for one phase. |
| `Full/analyze_full_mismatches.py` | Supports heuristic mismatch grouping; verify its paths before use. |
| `Raw/check_raw_data.py` | Checks Raw data consistency; verify its paths before use. |

### Input and output — English

#### `generate_pilot.py`

Input:

- `Data/Raw/RAW/`
- `Data/Improved/IMPROVED/`
- `Data/Annotations/Author 1 Responses.csv`
- `Data/Annotations/Author 2 Responses.csv`
- `Data/Annotations/Final Results.csv`
- `Data/Annotations/evaluation_metrics.yaml`

Output:

- `Data/Raw/pilot_sample_raw.csv`
- `Data/Raw/pilot_ground_truth_raw.csv`
- `Data/Raw/pilot_annotation_raw_author1.csv`
- `Data/Raw/pilot_annotation_raw_author2.csv`
- `Data/Improved/pilot_sample_improved.csv`
- `Data/Improved/pilot_ground_truth_improved.csv`
- `Data/Improved/pilot_annotation_improved_author1.csv`
- `Data/Improved/pilot_annotation_improved_author2.csv`

#### `kappa_pilot.py`

Input:

- Pilot annotation files in `Data/Raw`
- Pilot annotation files in `Data/Improved`

Output:

- `Data/Raw/kappa_scores_raw.csv`
- `Data/Improved/kappa_scores_improved.csv`

#### `Raw/create_full_ground_truth_raw.py`

Input:

- `Data/Annotations/Final Results.csv`

Output:

- `Data/Full/All/Raw/full_ground_truth_raw.csv`

#### `Improved/create_full_ground_truth_improved.py`

Input:

- `Data/Annotations/Final Results.csv`

Output:

- `Data/Full/All/Improved/full_ground_truth_improved.csv`

#### `create_full_samples.py`

Input:

- `Data/Raw/RAW/*.json`
- `Data/Improved/IMPROVED/*_improved.json`
- `Data/Full/All/Raw/full_ground_truth_raw.csv`
- `Data/Full/All/Improved/full_ground_truth_improved.csv`

Output:

- `Data/Full/All/Raw/full_sample_raw.csv`
- `Data/Full/All/Improved/full_sample_improved.csv`

#### `create_development_holdout_split.py`

Input:

- `Data/Full/All/Raw/full_sample_raw.csv`
- `Data/Full/All/Raw/full_ground_truth_raw.csv`
- `Data/Full/All/Improved/full_sample_improved.csv`
- `Data/Full/All/Improved/full_ground_truth_improved.csv`
- `Data/Raw/pilot_sample_raw.csv`
- `Data/Improved/pilot_sample_improved.csv`

Output:

- `Data/Full/Development/Raw/development_sample_raw.csv`
- `Data/Full/Development/Raw/development_ground_truth_raw.csv`
- `Data/Full/Development/Improved/development_sample_improved.csv`
- `Data/Full/Development/Improved/development_ground_truth_improved.csv`
- `Data/Full/Holdout/Raw/holdout_sample_raw.csv`
- `Data/Full/Holdout/Raw/holdout_ground_truth_raw.csv`
- `Data/Full/Holdout/Improved/holdout_sample_improved.csv`
- `Data/Full/Holdout/Improved/holdout_ground_truth_improved.csv`
- `Data/Full/Split/pilot_issue_keys.csv`
- `Data/Full/Split/development_issue_keys.csv`
- `Data/Full/Split/holdout_issue_keys.csv`
- `Data/Full/Split/split_assignment.csv`
- `Data/Full/Split/split_summary.csv`

#### `fix_full_ground_truth_headers.py`

Input and output in place:

- `Data/Full/All/Raw/full_ground_truth_raw.csv`
- `Data/Full/All/Improved/full_ground_truth_improved.csv`

Use only when duplicate headers exist.

#### `test_api.py`

Input:

- One row from Pilot, Development, or Pilot Validation
- The corresponding prompt file
- `.env`
- The matching Raw row when testing Improved

Output:

- Terminal output only
- No CSV file

#### `run_experiment.py`

| Phase | Version | Input | Output |
| --- | --- | --- | --- |
| Pilot | Raw | `Data/Raw/pilot_sample_raw.csv` | `Results/Raw/pilot_llm_output_raw.csv`, `Results/Raw/pilot_api_log_raw.csv` |
| Pilot | Improved | `Data/Improved/pilot_sample_improved.csv` and Raw Pilot context | `Results/Improved/pilot_llm_output_improved.csv`, `Results/Improved/pilot_api_log_improved.csv` |
| Development | Raw | `Data/Full/Development/Raw/development_sample_raw.csv` | `Results/Full/Development/Raw/development_llm_output_raw.csv`, `Results/Full/Development/Raw/development_api_log_raw.csv` |
| Development | Improved | `Data/Full/Development/Improved/development_sample_improved.csv` and Raw Development context | `Results/Full/Development/Improved/development_llm_output_improved.csv`, `Results/Full/Development/Improved/development_api_log_improved.csv` |
| Pilot Validation | Raw | `Data/Raw/pilot_sample_raw.csv` with Full configuration | `Results/Full/Pilot_Validation/Raw/pilot_validation_llm_output_raw.csv`, `Results/Full/Pilot_Validation/Raw/pilot_validation_api_log_raw.csv` |
| Pilot Validation | Improved | `Data/Improved/pilot_sample_improved.csv` and Raw Pilot context with Full configuration | `Results/Full/Pilot_Validation/Improved/pilot_validation_llm_output_improved.csv`, `Results/Full/Pilot_Validation/Improved/pilot_validation_api_log_improved.csv` |
| Holdout | Raw | `Data/Full/Holdout/Raw/holdout_sample_raw.csv` | `Results/Full/Holdout/Raw/holdout_llm_output_raw.csv`, `Results/Full/Holdout/Raw/holdout_api_log_raw.csv` |
| Holdout | Improved | `Data/Full/Holdout/Improved/holdout_sample_improved.csv` and Raw Holdout context | `Results/Full/Holdout/Improved/holdout_llm_output_improved.csv`, `Results/Full/Holdout/Improved/holdout_api_log_improved.csv` |

#### `compute_metric.py`

| Phase | Version | Prediction input | Ground Truth input | Output |
| --- | --- | --- | --- | --- |
| Pilot | Raw | `Results/Raw/pilot_llm_output_raw.csv` | `Data/Raw/pilot_ground_truth_raw.csv` | `Results/Raw/summary_raw.csv`, `Results/Raw/mismatch_analysis_raw.csv` |
| Pilot | Improved | `Results/Improved/pilot_llm_output_improved.csv` | `Data/Improved/pilot_ground_truth_improved.csv` | `Results/Improved/summary_improved.csv`, `Results/Improved/mismatch_analysis_improved.csv` |
| Development | Raw | `Results/Full/Development/Raw/development_llm_output_raw.csv` | `Data/Full/Development/Raw/development_ground_truth_raw.csv` | `Results/Full/Development/Raw/summary_development_raw.csv`, `Results/Full/Development/Raw/mismatch_analysis_development_raw.csv` |
| Development | Improved | `Results/Full/Development/Improved/development_llm_output_improved.csv` | `Data/Full/Development/Improved/development_ground_truth_improved.csv` | `Results/Full/Development/Improved/summary_development_improved.csv`, `Results/Full/Development/Improved/mismatch_analysis_development_improved.csv` |
| Pilot Validation | Raw | `Results/Full/Pilot_Validation/Raw/pilot_validation_llm_output_raw.csv` | `Data/Raw/pilot_ground_truth_raw.csv` | `Results/Full/Pilot_Validation/Raw/summary_pilot_validation_raw.csv`, `Results/Full/Pilot_Validation/Raw/mismatch_analysis_pilot_validation_raw.csv` |
| Pilot Validation | Improved | `Results/Full/Pilot_Validation/Improved/pilot_validation_llm_output_improved.csv` | `Data/Improved/pilot_ground_truth_improved.csv` | `Results/Full/Pilot_Validation/Improved/summary_pilot_validation_improved.csv`, `Results/Full/Pilot_Validation/Improved/mismatch_analysis_pilot_validation_improved.csv` |
| Holdout | Raw | `Results/Full/Holdout/Raw/holdout_llm_output_raw.csv` | `Data/Full/Holdout/Raw/holdout_ground_truth_raw.csv` | `Results/Full/Holdout/Raw/summary_holdout_raw.csv`, `Results/Full/Holdout/Raw/mismatch_analysis_holdout_raw.csv` |
| Holdout | Improved | `Results/Full/Holdout/Improved/holdout_llm_output_improved.csv` | `Data/Full/Holdout/Improved/holdout_ground_truth_improved.csv` | `Results/Full/Holdout/Improved/summary_holdout_improved.csv`, `Results/Full/Holdout/Improved/mismatch_analysis_holdout_improved.csv` |

#### `compare_raw_improved.py`

| Phase | Input | Output |
| --- | --- | --- |
| Pilot | Raw and Improved Pilot summaries | `Results/comparison_raw_vs_improved_pilot.csv` |
| Development | Raw and Improved Development summaries | `Results/Full/Development/comparison_raw_vs_improved_development.csv` |
| Pilot Validation | Raw and Improved Pilot Validation summaries | `Results/Full/Pilot_Validation/comparison_raw_vs_improved_pilot_validation.csv` |
| Holdout | Raw and Improved Holdout summaries | `Results/Full/Holdout/comparison_raw_vs_improved_holdout.csv` |

### Important notes — English

- Do not commit `.env`.
- Do not provide Ground Truth to the LLM prompt.
- Do not modify frozen Pilot prompts.
- Do not use `test_api.py` or `--limit` on Holdout.
- Do not recreate the split after Holdout evaluation.
- Do not tune prompts or rules using Holdout mismatches.
- The current project has already completed Holdout evaluation. Destructive data
  generation and Holdout commands are for clean reproduction only.

## Tiếng Việt

### Mục đích — Tiếng Việt

Thư mục `Scripts` dùng để tạo dữ liệu, chạy thí nghiệm LLM, tính metric, so sánh
Raw với Improved và hoàn thành quy trình Pilot–Development–Pilot Validation–
Holdout.

### Tóm tắt script — Tiếng Việt

| Script | Chức năng |
| --- | --- |
| `generate_pilot.py` | Tạo sample, Ground Truth và annotation Pilot. |
| `kappa_pilot.py` | Tính Cohen's Kappa giữa hai người gán nhãn Pilot. |
| `Raw/create_full_ground_truth_raw.py` | Tạo Ground Truth Full Raw gồm 139 case. |
| `Improved/create_full_ground_truth_improved.py` | Tạo Ground Truth Full Improved gồm 139 case. |
| `create_full_samples.py` | Tạo sample Full Raw và Improved. |
| `create_development_holdout_split.py` | Chia 26 Pilot, 75 Development và 38 Holdout. |
| `fix_full_ground_truth_headers.py` | Sửa header Ground Truth bị trùng khi cần. |
| `test_api.py` | Test một case ngoài Holdout, không tạo CSV. |
| `run_experiment.py` | Chạy LLM cho từng phase. |
| `compute_metric.py` | Tính Accuracy, Kappa, confusion matrix, mismatch, token và cost. |
| `compare_raw_improved.py` | So sánh Raw và Improved trong cùng phase. |
| `Full/analyze_full_mismatches.py` | Hỗ trợ phân nhóm mismatch; kiểm tra đường dẫn trước khi dùng. |
| `Raw/check_raw_data.py` | Kiểm tra dữ liệu Raw; kiểm tra đường dẫn trước khi dùng. |

### Quy tắc input và output — Tiếng Việt

- `sample_*.csv` là input của LLM.
- `ground_truth_*.csv` chỉ dùng khi tính metric.
- `run_experiment.py` tạo `*_llm_output_*.csv` và `*_api_log_*.csv`.
- `compute_metric.py` tạo `summary_*.csv` và `mismatch_analysis_*.csv`.
- `compare_raw_improved.py` tạo file comparison của từng phase.
- Improved dùng thêm Raw report cùng issue key làm context.
- `test_api.py` chỉ in kết quả ra terminal.
- Holdout yêu cầu `--confirm-holdout-final` và không cho dùng `--limit`.

### Lưu ý quan trọng — Tiếng Việt

- Không commit `.env`.
- Không đưa Ground Truth vào prompt LLM.
- Không sửa prompt Pilot đã đóng băng.
- Không dùng `test_api.py` hoặc `--limit` trên Holdout.
- Không tạo lại phép chia sau khi đã chạy Holdout.
- Không tuning bằng mismatch Holdout.
- Project hiện tại đã hoàn thành Holdout. Các lệnh tạo lại dữ liệu và Holdout chỉ
  dùng khi tái lập sạch từ đầu.
