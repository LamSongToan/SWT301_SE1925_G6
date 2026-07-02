# Results/Improved README

> **EN:** This folder stores LLM outputs and evaluation results for the Improved
> Mojira bug report dataset.
>
> **VI:** Thư mục này lưu trữ output của LLM và kết quả đánh giá cho bộ dữ liệu
> Mojira phiên bản Improved.

---

## 1. Purpose

**EN:** `Results/Improved/` contains the generated prediction files, API logs,
summary metrics, and mismatch analysis files for the Improved experiment.

The results are produced after running the LLM-based reproducibility classifier
on the Improved dataset and evaluating the predictions against manual ground
truth labels.

**VI:** `Results/Improved/` chứa các file dự đoán do LLM tạo ra, log API,
file tổng hợp metric, và file phân tích mismatch cho thí nghiệm Improved.

Các kết quả này được tạo sau khi chạy bộ phân loại khả năng tái hiện lỗi bằng
LLM trên bộ dữ liệu Improved và so sánh dự đoán với nhãn ground truth thủ công.

---

## 2. Folder Structure

Results/Improved/
├── README.md
├── .gitkeep
├── pilot_llm_output_improved.csv
├── pilot_api_log_improved.csv
├── summary_improved.csv
├── mismatch_analysis_improved.csv
├── full_llm_output_improved.csv
├── full_api_log_improved.csv
├── summary_full_improved.csv
└── mismatch_analysis_full_improved.csv

**VI:** Cấu trúc trên gồm file README, file `.gitkeep`, output pilot,
output full, API log, summary metric, và mismatch analysis của phiên bản
Improved.

---

## 3. File Description

### 3.1 pilot_llm_output_improved.csv

**EN:** Contains LLM predictions for the Improved pilot experiment.

**VI:** Chứa dự đoán của LLM cho thí nghiệm pilot của bộ Improved.

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

### 3.2 pilot_api_log_improved.csv

**EN:** Contains detailed API execution logs for the Improved pilot experiment.

**VI:** Chứa log chi tiết quá trình gọi API cho thí nghiệm pilot Improved.

This file is useful for checking:

- processing order
- status of each API call
- prediction result
- error message, if any
- token usage
- cost per call

### 3.3 summary_improved.csv

**EN:** Contains pilot-level evaluation metrics for the Improved dataset.

**VI:** Chứa các metric đánh giá ở giai đoạn pilot cho bộ Improved.

Current pilot result:

Total cases       : 26
Accuracy          : 0.7308
Cohen's Kappa     : 0.0000
Threshold         : 0.70
Threshold passed  : False
Mismatch cases    : 7

### 3.4 mismatch_analysis_improved.csv

**EN:** Contains pilot cases where the LLM prediction does not match the manual
ground truth label.

**VI:** Chứa các case pilot mà dự đoán của LLM không khớp với nhãn ground truth
thủ công.

This file is used to inspect why the LLM classified a report incorrectly.

### 3.5 full_llm_output_improved.csv

**EN:** Contains LLM predictions for the full Improved experiment.

**VI:** Chứa dự đoán của LLM cho full experiment của bộ Improved.

Typical content includes the same type of columns as
`pilot_llm_output_improved.csv`.

### 3.6 full_api_log_improved.csv

**EN:** Contains detailed API execution logs for the full Improved experiment.

**VI:** Chứa log chi tiết quá trình gọi API cho full experiment Improved.

This file is useful for checking whether all full cases were processed
successfully.

### 3.7 summary_full_improved.csv

**EN:** Contains full-level evaluation metrics for the Improved dataset.

**VI:** Chứa các metric đánh giá ở giai đoạn full cho bộ Improved.

Current full result:

Total cases       : 139
Accuracy          : 0.6906
Cohen's Kappa     : 0.0592
Threshold         : 0.70
Threshold passed  : False
Mismatch cases    : 43

### 3.8 mismatch_analysis_full_improved.csv

**EN:** Contains full experiment cases where the LLM prediction does not match
the manual ground truth label.

**VI:** Chứa các case full mà dự đoán của LLM không khớp với nhãn ground truth
thủ công.

This file is important for error analysis and discussion in the report.

### 3.9 .gitkeep

**EN:** Keeps the `Results/Improved/` folder visible in Git even when generated
CSV files are ignored or removed.

**VI:** Giữ thư mục `Results/Improved/` xuất hiện trong Git kể cả khi các file
CSV kết quả bị ignore hoặc bị xóa.

---

## 4. Experiment Result Summary

### 4.1 Pilot Improved result

Model             : gpt-4o-mini-2024-07-18
Prompt version    : v2
Total cases       : 26
Accuracy          : 0.7308
Cohen's Kappa     : 0.0000
Threshold         : 0.70
Threshold passed  : False
Mismatch cases    : 7

**VI:** Ở pilot Improved, Accuracy đạt `0.7308`, nhưng Cohen's Kappa bằng
`0.0000`, nên chưa đạt ngưỡng `0.70`.

### 4.2 Full Improved result

Model             : gpt-4o-mini-2024-07-18
Prompt version    : v2
Total cases       : 139
Accuracy          : 0.6906
Cohen's Kappa     : 0.0592
Threshold         : 0.70
Threshold passed  : False
Mismatch cases    : 43

**VI:** Ở full Improved, Accuracy đạt `0.6906`, Cohen's Kappa đạt `0.0592`,
nên cũng chưa đạt ngưỡng `0.70`.

---

## 5. Interpretation Notes

**EN:** The Improved reports contain structured fields such as
`Steps to Reproduce`, `Observed Behavior`, `Expected Behavior`, and
`Environment`. However, the LLM showed a strong tendency to classify Improved
reports as `Executable`.

This explains why Accuracy can look acceptable while Cohen's Kappa remains low.
Kappa penalizes agreement that can be explained by label imbalance or biased
prediction behavior.

**VI:** Báo cáo Improved có các trường được cấu trúc như `Steps to Reproduce`,
`Observed Behavior`, `Expected Behavior`, và `Environment`. Tuy nhiên, LLM có
xu hướng mạnh khi phân loại các báo cáo Improved thành `Executable`.

Điều này giải thích vì sao Accuracy có thể nhìn tương đối ổn nhưng Cohen's
Kappa vẫn thấp. Kappa phạt các trường hợp đồng thuận có thể đến từ mất cân bằng
nhãn hoặc xu hướng dự đoán lệch của mô hình.

---

## 6. Usage

### 6.1 Run Improved pilot experiment

.\.venv\Scripts\python.exe Scripts\run_experiment.py --version improved --phase pilot
.\.venv\Scripts\python.exe Scripts\compute_metric.py --version improved --phase pilot

### 6.2 Run Improved full experiment

.\.venv\Scripts\python.exe Scripts\run_experiment.py --version improved --phase full
.\.venv\Scripts\python.exe Scripts\compute_metric.py --version improved --phase full

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

- **EN:** Source data for Improved reports is stored in `Data/Improved/`.
- **VI:** Dữ liệu nguồn của báo cáo Improved nằm trong `Data/Improved/`.

- **EN:** The final comparison file is stored in the parent `Results/` folder.
- **VI:** File so sánh cuối cùng được lưu ở thư mục cha `Results/`.

Examples:

Results/comparison_raw_vs_improved_pilot.csv
Results/comparison_raw_vs_improved_full.csv

---

## 8. Scope

This README only describes the `Results/Improved/` folder.

It does not cover:

- `Results/Raw/`
- `Data/Raw/`
- `Data/Improved/`
- `Figures/`
- analysis notebooks such as `pilot_analysis.ipynb` or `full_analysis.ipynb`

**VI:** README này chỉ mô tả thư mục `Results/Improved/`. README này không mô
tả `Results/Raw/`, `Data/Raw/`, `Data/Improved/`, `Figures/`, hoặc các notebook
phân tích.
