# Results/Raw README

> **EN:** This folder stores LLM outputs and evaluation results for the Raw
> Mojira bug report dataset.
>
> **VI:** Thư mục này lưu trữ output của LLM và kết quả đánh giá cho bộ dữ liệu
> Mojira phiên bản Raw.

---

## 1. Purpose

**EN:** `Results/Raw/` contains the generated prediction files, API logs,
summary metrics, and mismatch analysis files for the Raw experiment.

The results are produced after running the LLM-based reproducibility classifier
on the Raw dataset and evaluating the predictions against manual ground truth
labels.

**VI:** `Results/Raw/` chứa các file dự đoán do LLM tạo ra, log API, file tổng
hợp metric, và file phân tích mismatch cho thí nghiệm Raw.

Các kết quả này được tạo sau khi chạy bộ phân loại khả năng tái hiện lỗi bằng
LLM trên bộ dữ liệu Raw và so sánh dự đoán với nhãn ground truth thủ công.

---

## 2. Folder Structure

Results/Raw/
├── README.md
├── .gitkeep
├── pilot_llm_output_raw.csv
├── pilot_api_log_raw.csv
├── summary_raw.csv
├── mismatch_analysis_raw.csv
├── full_llm_output_raw.csv
├── full_api_log_raw.csv
├── summary_full_raw.csv
└── mismatch_analysis_full_raw.csv

**VI:** Cấu trúc trên gồm file README, file `.gitkeep`, output pilot, output
full, API log, summary metric, và mismatch analysis của phiên bản Raw.

---

## 3. File Description

### 3.1 pilot_llm_output_raw.csv

**EN:** Contains LLM predictions for the Raw pilot experiment.

**VI:** Chứa dự đoán của LLM cho thí nghiệm pilot của bộ Raw.

Typical content includes:

- `issue_key`
- `s2r_label`
- `reason`
- `status`
- `model`
- `prompt_version`
- token usage
- cost
- raw response

### 3.2 pilot_api_log_raw.csv

**EN:** Contains detailed API execution logs for the Raw pilot experiment.

**VI:** Chứa log chi tiết quá trình gọi API cho thí nghiệm pilot Raw.

This file is useful for checking:

- processing order
- status of each API call
- prediction result
- error message, if any
- token usage
- cost per call

### 3.3 summary_raw.csv

**EN:** Contains pilot-level evaluation metrics for the Raw dataset.

**VI:** Chứa các metric đánh giá ở giai đoạn pilot cho bộ Raw.

Current pilot result:

Total cases       : 26
Accuracy          : 0.6923
Cohen's Kappa     : 0.3247
Threshold         : 0.70
Threshold passed  : False
Mismatch cases    : 8

### 3.4 mismatch_analysis_raw.csv

**EN:** Contains pilot cases where the LLM prediction does not match the manual
ground truth label.

**VI:** Chứa các case pilot mà dự đoán của LLM không khớp với nhãn ground truth
thủ công.

This file is used to inspect why the LLM classified a report incorrectly.

### 3.5 full_llm_output_raw.csv

**EN:** Contains LLM predictions for the full Raw experiment.

**VI:** Chứa dự đoán của LLM cho full experiment của bộ Raw.

Typical content includes the same type of columns as `pilot_llm_output_raw.csv`.

### 3.6 full_api_log_raw.csv

**EN:** Contains detailed API execution logs for the full Raw experiment.

**VI:** Chứa log chi tiết quá trình gọi API cho full experiment Raw.

This file is useful for checking whether all full cases were processed
successfully.

### 3.7 summary_full_raw.csv

**EN:** Contains full-level evaluation metrics for the Raw dataset.

**VI:** Chứa các metric đánh giá ở giai đoạn full cho bộ Raw.

Current full result:

Total cases       : 139
Accuracy          : 0.7338
Cohen's Kappa     : 0.3358
Threshold         : 0.70
Threshold passed  : False
Mismatch cases    : 37

### 3.8 mismatch_analysis_full_raw.csv

**EN:** Contains full experiment cases where the LLM prediction does not match
the manual ground truth label.

**VI:** Chứa các case full mà dự đoán của LLM không khớp với nhãn ground truth
thủ công.

This file is important for error analysis and discussion in the report.

### 3.9 .gitkeep

**EN:** Keeps the `Results/Raw/` folder visible in Git even when generated CSV
files are ignored or removed.

**VI:** Giữ thư mục `Results/Raw/` xuất hiện trong Git kể cả khi các file CSV
kết quả bị ignore hoặc bị xóa.

---

## 4. Experiment Result Summary

### 4.1 Pilot Raw result

Model             : gpt-4o-mini-2024-07-18
Prompt version    : v2
Total cases       : 26
Accuracy          : 0.6923
Cohen's Kappa     : 0.3247
Threshold         : 0.70
Threshold passed  : False
Mismatch cases    : 8

**VI:** Ở pilot Raw, Accuracy đạt `0.6923`, Cohen's Kappa đạt `0.3247`, nên
chưa đạt ngưỡng `0.70`.

### 4.2 Full Raw result

Model             : gpt-4o-mini-2024-07-18
Prompt version    : v2
Total cases       : 139
Accuracy          : 0.7338
Cohen's Kappa     : 0.3358
Threshold         : 0.70
Threshold passed  : False
Mismatch cases    : 37

**VI:** Ở full Raw, Accuracy đạt `0.7338`, Cohen's Kappa đạt `0.3358`, nên
cũng chưa đạt ngưỡng `0.70`.

---

## 5. Interpretation Notes

**EN:** The Raw reports are original bug reports before improvement. Compared
with the Improved result, the Raw full experiment achieved higher Accuracy and
higher Cohen's Kappa.

However, the Raw result still did not reach the target threshold of Cohen's
Kappa `0.70`. This means the current LLM classification setup did not achieve
sufficient agreement with manual/developer review.

**VI:** Báo cáo Raw là báo cáo lỗi gốc trước khi được cải thiện. So với kết quả
Improved, full experiment của Raw đạt Accuracy và Cohen's Kappa cao hơn.

Tuy nhiên, kết quả Raw vẫn chưa đạt ngưỡng mục tiêu Cohen's Kappa `0.70`. Điều
này nghĩa là thiết lập phân loại bằng LLM hiện tại chưa đạt mức đồng thuận đủ
cao với manual/developer review.

---

## 6. Usage

### 6.1 Run Raw pilot experiment

.\.venv\Scripts\python.exe Scripts\run_experiment.py --version raw --phase pilot
.\.venv\Scripts\python.exe Scripts\compute_metric.py --version raw --phase pilot

### 6.2 Run Raw full experiment

.\.venv\Scripts\python.exe Scripts\run_experiment.py --version raw --phase full
.\.venv\Scripts\python.exe Scripts\compute_metric.py --version raw --phase full

### 6.3 Compare Raw and Improved results

.\.venv\Scripts\python.exe Scripts\compare_raw_improved.py --phase pilot
.\.venv\Scripts\python.exe Scripts\compare_raw_improved.py --phase full

---

## 7. Important Notes

- **EN:** These files are generated outputs, not source dataset files.
- **VI:** Các file trong thư mục này là output được tạo ra, không phải dữ liệu
  nguồn ban đầu.

- **EN:** Do not manually edit result CSV files unless documenting a correction.
- **VI:** Không chỉnh sửa thủ công các file CSV kết quả, trừ khi đang ghi nhận
  một chỉnh sửa có kiểm soát.

- **EN:** Source data for Raw reports is stored in `Data/Raw/`.
- **VI:** Dữ liệu nguồn của báo cáo Raw nằm trong `Data/Raw/`.

- **EN:** The final comparison file is stored in the parent `Results/` folder.
- **VI:** File so sánh cuối cùng được lưu ở thư mục cha `Results/`.

Examples:

Results/comparison_raw_vs_improved_pilot.csv
Results/comparison_raw_vs_improved_full.csv

---

## 8. Scope

This README only describes the `Results/Raw/` folder.

It does not cover:

- `Results/Improved/`
- `Data/Raw/`
- `Data/Improved/`
- `Figures/`
- analysis notebooks such as `pilot_analysis.ipynb` or `full_analysis.ipynb`

**VI:** README này chỉ mô tả thư mục `Results/Raw/`. README này không mô tả
`Results/Improved/`, `Data/Raw/`, `Data/Improved/`, `Figures/`, hoặc các
notebook phân tích.
