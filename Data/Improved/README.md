# Data/Improved README

> **EN:** This folder contains the Improved version of the Mojira bug report dataset used for LLM-based reproducibility classification.
>
> **VI:** Thư mục này chứa phiên bản Improved của bộ dữ liệu báo cáo lỗi Mojira, dùng để phân loại khả năng tái hiện lỗi bằng LLM.

---

## 1. Purpose

**EN:** `Data/Improved/` stores the improved bug reports, pilot samples, full samples, manual ground truth labels, author annotations, and inter-annotator agreement results for the Improved dataset.

This dataset is used to evaluate whether an LLM can classify bug reports as:

- `Executable`
- `Non-Executable`

The LLM predictions are compared against developer/manual review labels using Accuracy and Cohen's Kappa.

**VI:** `Data/Improved/` lưu trữ các báo cáo lỗi đã được cải thiện, mẫu pilot, mẫu full, nhãn ground truth thủ công, annotation của từng author, và kết quả đo độ đồng thuận giữa annotators cho bộ dữ liệu Improved.

Bộ dữ liệu này dùng để đánh giá liệu LLM có thể phân loại báo cáo lỗi thành:

- `Executable`
- `Non-Executable`

Kết quả dự đoán của LLM được so sánh với nhãn manual review/developer review bằng Accuracy và Cohen's Kappa.

---

## 2. Folder Structure

Data/Improved/
├── IMPROVED/
│   └── *_improved.json
│
├── README.md
├── full_sample_improved.csv
├── full_ground_truth_improved.csv
├── pilot_sample_improved.csv
├── pilot_ground_truth_improved.csv
├── pilot_annotation_improved_author1.csv
├── pilot_annotation_improved_author2.csv
└── kappa_scores_improved.csv

**VI:** Cấu trúc trên cho thấy thư mục `Data/Improved/` gồm dữ liệu JSON Improved, các file sample cho LLM, các file ground truth, annotation của hai author, và file tính Cohen's Kappa giữa annotators.

---

## 3. File Description

### 3.1 IMPROVED folder

**EN:** Contains 139 improved Mojira bug report JSON files. Each file is expected to follow the pattern `MC-xxxxx_improved.json`.

**VI:** Chứa 139 file JSON báo cáo lỗi Mojira đã được cải thiện. Tên file thường có dạng `MC-xxxxx_improved.json`.

### 3.2 full_sample_improved.csv

**EN:** Contains 139 full Improved bug reports used as LLM input for the full experiment.

**VI:** Chứa 139 báo cáo Improved dùng làm input cho LLM trong full experiment.

### 3.3 full_ground_truth_improved.csv

**EN:** Contains 139 manual ground truth labels for the full Improved dataset. This file is used by `compute_metric.py` for evaluation only. It must not be used as LLM input.

**VI:** Chứa 139 nhãn ground truth thủ công cho bộ Improved full. File này chỉ dùng để đánh giá bằng `compute_metric.py`, không được dùng làm input cho LLM.

### 3.4 pilot_sample_improved.csv

**EN:** Contains 26 Improved pilot reports used as LLM input for the pilot experiment.

**VI:** Chứa 26 báo cáo Improved dùng làm input cho LLM trong pilot experiment.

### 3.5 pilot_ground_truth_improved.csv

**EN:** Contains 26 manual ground truth labels for the Improved pilot set. This file is used by `compute_metric.py` for pilot evaluation.

**VI:** Chứa 26 nhãn ground truth thủ công cho pilot Improved. File này dùng để tính metric ở giai đoạn pilot.

### 3.6 pilot_annotation_improved_author1.csv

**EN:** Contains the pilot annotations provided by Author 1 for the Improved dataset.

**VI:** Chứa annotation pilot của Author 1 cho bộ dữ liệu Improved.

### 3.7 pilot_annotation_improved_author2.csv

**EN:** Contains the pilot annotations provided by Author 2 for the Improved dataset.

**VI:** Chứa annotation pilot của Author 2 cho bộ dữ liệu Improved.

### 3.8 kappa_scores_improved.csv

**EN:** Contains the inter-annotator agreement results for the Improved pilot set.

**VI:** Chứa kết quả đo độ đồng thuận giữa annotators cho pilot Improved.

---

## 4. Main Columns in LLM Input Files

This section applies to:

- `pilot_sample_improved.csv`
- `full_sample_improved.csv`

### 4.1 Issue Key

**EN:** Mojira issue key, such as `MC-300962`.

**VI:** Mã issue trên Mojira, ví dụ `MC-300962`.

### 4.2 Summary

**EN:** Short bug report title.

**VI:** Tiêu đề ngắn của bug report.

### 4.3 Type

**EN:** Issue type, usually `Bug`.

**VI:** Loại issue, thường là `Bug`.

### 4.4 Affects Version/s

**EN:** Minecraft version or versions affected by the bug.

**VI:** Phiên bản Minecraft bị ảnh hưởng bởi lỗi.

### 4.5 Labels

**EN:** Issue labels if available.

**VI:** Nhãn của issue nếu có.

### 4.6 Confirmation Status

**EN:** Confirmation status from the issue tracker.

**VI:** Trạng thái xác nhận từ issue tracker.

### 4.7 Category

**EN:** Bug category if available.

**VI:** Danh mục lỗi nếu có.

### 4.8 Resolution

**EN:** Resolution status from the issue tracker.

**VI:** Trạng thái xử lý hoặc kết luận của issue.

### 4.9 Fix Version/s

**EN:** Version or versions where the bug is fixed, if available.

**VI:** Phiên bản sửa lỗi nếu có.

### 4.10 Description

**EN:** Improved description of the bug report.

**VI:** Mô tả đã được cải thiện của bug report.

### 4.11 Steps to Reproduce

**EN:** Improved reproduction steps.

**VI:** Các bước tái hiện lỗi đã được cải thiện.

### 4.12 Observed Behavior

**EN:** Actual observed incorrect behavior.

**VI:** Hành vi lỗi thực tế quan sát được.

### 4.13 Expected Behavior

**EN:** Expected correct behavior.

**VI:** Hành vi đúng mong đợi.

### 4.14 Environment

**EN:** Environment information, such as Minecraft version.

**VI:** Thông tin môi trường, ví dụ phiên bản Minecraft.

---

## 5. Main Columns in Ground Truth and Annotation Files

This section applies to:

- `pilot_ground_truth_improved.csv`
- `full_ground_truth_improved.csv`
- `pilot_annotation_improved_author1.csv`
- `pilot_annotation_improved_author2.csv`

### 5.1 BUG-ID

**EN:** Bug report identifier with the Improved suffix.

**VI:** Mã bug report, thường có hậu tố Improved.

### 5.2 S2R Label

**EN:** Final reproducibility label. The expected values are `Executable` and `Non-Executable`.

**VI:** Nhãn khả năng tái hiện. Giá trị mong đợi là `Executable` và `Non-Executable`.

### 5.3 S2R Irrep Category

**EN:** Irreproducibility category if the report is not executable.

**VI:** Nhóm nguyên nhân không tái hiện được nếu report không executable.

### 5.4 Reason

**EN:** Explanation for the S2R label or category.

**VI:** Lý do cho nhãn hoặc category.

### 5.5 OB Category

**EN:** Observed Behavior category.

**VI:** Nhóm đánh giá Observed Behavior.

### 5.6 OB Label

**EN:** Observed Behavior quality label.

**VI:** Nhãn chất lượng của Observed Behavior.

### 5.7 EB Category

**EN:** Expected Behavior category.

**VI:** Nhóm đánh giá Expected Behavior.

### 5.8 EB Label

**EN:** Expected Behavior quality label.

**VI:** Nhãn chất lượng của Expected Behavior.

---

## 6. Dataset Statistics

### 6.1 Pilot ground truth

- **File:** `pilot_ground_truth_improved.csv`
- **Total cases:** 26
- **Executable:** 19
- **Non-Executable:** 7

### 6.2 Full ground truth

- **File:** `full_ground_truth_improved.csv`
- **Total cases:** 139
- **Executable:** 94
- **Non-Executable:** 45

### 6.3 Author 1 pilot annotation

- **File:** `pilot_annotation_improved_author1.csv`
- **Total cases:** 26
- **Executable:** 19
- **Non-Executable:** 7

### 6.4 Author 2 pilot annotation

- **File:** `pilot_annotation_improved_author2.csv`
- **Total cases:** 26
- **Executable:** 18
- **Non-Executable:** 8

### 6.5 Pilot inter-annotator agreement

N            : 26
Cohen Kappa  : 0.7524
Agreement    : 22/26

**VI:** Kết quả trên cho thấy hai annotators có mức độ đồng thuận tốt ở pilot Improved, với Cohen's Kappa là `0.7524`.

---

## 7. Usage in Experiment

### 7.1 Use sample files as LLM input

Use these files as input for `run_experiment.py`:

Data/Improved/pilot_sample_improved.csv
Data/Improved/full_sample_improved.csv

**VI:** Dùng các file sample ở trên làm input cho LLM.

### 7.2 Use ground truth files only for evaluation

Use these files only for `compute_metric.py`:

Data/Improved/pilot_ground_truth_improved.csv
Data/Improved/full_ground_truth_improved.csv

**VI:** Chỉ dùng các file ground truth ở trên để đánh giá kết quả, không dùng làm input cho LLM.

### 7.3 Recommended commands

Run the Improved pilot experiment:

.\.venv\Scripts\python.exe Scripts\run_experiment.py --version improved --phase pilot
.\.venv\Scripts\python.exe Scripts\compute_metric.py --version improved --phase pilot

Run the Improved full experiment:

.\.venv\Scripts\python.exe Scripts\run_experiment.py --version improved --phase full
.\.venv\Scripts\python.exe Scripts\compute_metric.py --version improved --phase full

---

## 8. Important Notes

- **EN:** Do not use `pilot_ground_truth_improved.csv` or `full_ground_truth_improved.csv` as LLM input because they contain manual labels and annotation information.
- **VI:** Không dùng `pilot_ground_truth_improved.csv` hoặc `full_ground_truth_improved.csv` làm input cho LLM vì các file này chứa nhãn thủ công và thông tin annotation.

- **EN:** Use `pilot_sample_improved.csv` and `full_sample_improved.csv` as the LLM input files.
- **VI:** Dùng `pilot_sample_improved.csv` và `full_sample_improved.csv` làm input cho LLM.

- **EN:** The Improved reports contain structured fields such as `Steps to Reproduce`, `Observed Behavior`, `Expected Behavior`, and `Environment`.
- **VI:** Báo cáo Improved có các trường đã được cấu trúc như `Steps to Reproduce`, `Observed Behavior`, `Expected Behavior`, và `Environment`.

- **EN:** The file `kappa_scores_improved.csv` is used to report inter-annotator agreement for the pilot annotation process.
- **VI:** File `kappa_scores_improved.csv` dùng để báo cáo độ đồng thuận giữa annotators trong giai đoạn pilot.

- **EN:** Result files generated by LLM experiments should be stored in `Results/Improved/`, not in `Data/Improved/`.
- **VI:** Các file kết quả do LLM tạo ra nên được lưu trong `Results/Improved/`, không lưu trong `Data/Improved/`.

---

## 9. Related Output Folder

The output files for Improved experiments are expected to be stored in:

Results/Improved/

Typical output files include:

pilot_llm_output_improved.csv
pilot_api_log_improved.csv
summary_improved.csv
mismatch_analysis_improved.csv

full_llm_output_improved.csv
full_api_log_improved.csv
summary_full_improved.csv
mismatch_analysis_full_improved.csv

**VI:** Các file kết quả của thí nghiệm Improved nên được lưu tại `Results/Improved/`.

---

## 10. Scope

This README only describes the `Data/Improved/` folder.

It does not cover:

- `Data/Raw/`
- `Results/`
- `Figures/`
- analysis notebooks such as `pilot_analysis.ipynb` or `full_analysis.ipynb`

**VI:** README này chỉ mô tả thư mục `Data/Improved/`. README này không mô tả `Data/Raw/`, `Results/`, `Figures/`, hoặc các notebook phân tích.
