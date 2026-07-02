# Data/Raw README

> **EN:** This folder contains the Raw version of the Mojira bug report dataset
> used for LLM-based reproducibility classification.
>
> **VI:** Thư mục này chứa phiên bản Raw của bộ dữ liệu báo cáo lỗi Mojira,
> dùng để phân loại khả năng tái hiện lỗi bằng LLM.

---

## 1. Purpose

**EN:** `Data/Raw/` stores the original/raw Mojira bug reports, pilot samples,
full samples, manual ground truth labels, author annotations, and
inter-annotator agreement results for the Raw dataset.

This dataset is used to evaluate whether an LLM can classify bug reports as:

- `Executable`
- `Non-Executable`

The LLM predictions are compared against developer/manual review labels using
Accuracy and Cohen's Kappa.

**VI:** `Data/Raw/` lưu trữ các báo cáo lỗi Mojira gốc/chưa cải thiện,
mẫu pilot, mẫu full, nhãn ground truth thủ công, annotation của từng author,
và kết quả đo độ đồng thuận giữa annotators cho bộ dữ liệu Raw.

Bộ dữ liệu này dùng để đánh giá liệu LLM có thể phân loại báo cáo lỗi thành:

- `Executable`
- `Non-Executable`

Kết quả dự đoán của LLM được so sánh với nhãn manual review/developer review
bằng Accuracy và Cohen's Kappa.

---

## 2. Folder Structure

Data/Raw/
├── RAW/
│   └── *.json
│
├── README.md
├── full_sample_raw.csv
├── full_ground_truth_raw.csv
├── pilot_sample_raw.csv
├── pilot_ground_truth_raw.csv
├── pilot_annotation_raw_author1.csv
├── pilot_annotation_raw_author2.csv
└── kappa_scores_raw.csv

**VI:** Cấu trúc trên cho thấy thư mục `Data/Raw/` gồm dữ liệu JSON Raw,
các file sample cho LLM, các file ground truth, annotation của hai author,
và file tính Cohen's Kappa giữa annotators.

---

## 3. File Description

### 3.1 RAW folder

**EN:** Contains 139 original Mojira bug report JSON files. Each file is expected
to follow the pattern `MC-xxxxx.json`.

**VI:** Chứa 139 file JSON báo cáo lỗi Mojira gốc. Tên file thường có dạng
`MC-xxxxx.json`.

### 3.2 full_sample_raw.csv

**EN:** Contains 139 full Raw bug reports used as LLM input for the full
experiment.

**VI:** Chứa 139 báo cáo Raw dùng làm input cho LLM trong full experiment.

### 3.3 full_ground_truth_raw.csv

**EN:** Contains 139 manual ground truth labels for the full Raw dataset.
This file is used by `compute_metric.py` for evaluation only. It must not be
used as LLM input.

**VI:** Chứa 139 nhãn ground truth thủ công cho bộ Raw full. File này chỉ dùng
để đánh giá bằng `compute_metric.py`, không được dùng làm input cho LLM.

### 3.4 pilot_sample_raw.csv

**EN:** Contains 26 Raw pilot reports used as LLM input for the pilot experiment.

**VI:** Chứa 26 báo cáo Raw dùng làm input cho LLM trong pilot experiment.

### 3.5 pilot_ground_truth_raw.csv

**EN:** Contains 26 manual ground truth labels for the Raw pilot set.
This file is used by `compute_metric.py` for pilot evaluation.

**VI:** Chứa 26 nhãn ground truth thủ công cho pilot Raw. File này dùng để tính
metric ở giai đoạn pilot.

### 3.6 pilot_annotation_raw_author1.csv

**EN:** Contains the pilot annotations provided by Author 1 for the Raw dataset.

**VI:** Chứa annotation pilot của Author 1 cho bộ dữ liệu Raw.

### 3.7 pilot_annotation_raw_author2.csv

**EN:** Contains the pilot annotations provided by Author 2 for the Raw dataset.

**VI:** Chứa annotation pilot của Author 2 cho bộ dữ liệu Raw.

### 3.8 kappa_scores_raw.csv

**EN:** Contains the inter-annotator agreement results for the Raw pilot set.

**VI:** Chứa kết quả đo độ đồng thuận giữa annotators cho pilot Raw.

---

## 4. Main Columns in LLM Input Files

This section applies to:

- `pilot_sample_raw.csv`
- `full_sample_raw.csv`

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

**EN:** Original/raw description of the bug report.

**VI:** Mô tả gốc/chưa cải thiện của bug report.

---

## 5. Main Columns in Ground Truth and Annotation Files

This section applies to:

- `pilot_ground_truth_raw.csv`
- `full_ground_truth_raw.csv`
- `pilot_annotation_raw_author1.csv`
- `pilot_annotation_raw_author2.csv`

### 5.1 BUG-ID

**EN:** Bug report identifier with the Raw suffix.

**VI:** Mã bug report, thường có hậu tố Raw.

### 5.2 S2R Label

**EN:** Final reproducibility label. The expected values are `Executable`
and `Non-Executable`.

**VI:** Nhãn khả năng tái hiện. Giá trị mong đợi là `Executable`
và `Non-Executable`.

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

- **File:** `pilot_ground_truth_raw.csv`
- **Total cases:** 26
- **Executable:** 10
- **Non-Executable:** 16

### 6.2 Full ground truth

- **File:** `full_ground_truth_raw.csv`
- **Total cases:** 139
- **Executable:** 40
- **Non-Executable:** 99

### 6.3 Author 1 pilot annotation

- **File:** `pilot_annotation_raw_author1.csv`
- **Total cases:** 26
- **Executable:** 10
- **Non-Executable:** 16

### 6.4 Author 2 pilot annotation

- **File:** `pilot_annotation_raw_author2.csv`
- **Total cases:** 26
- **Executable:** 9
- **Non-Executable:** 17

### 6.5 Pilot inter-annotator agreement

N            : 26
Cohen Kappa  : 0.7647
Agreement    : 22/26

**VI:** Kết quả trên cho thấy hai annotators có mức độ đồng thuận tốt ở pilot
Raw, với Cohen's Kappa là `0.7647`.

---

## 7. Usage in Experiment

### 7.1 Use sample files as LLM input

Use these files as input for `run_experiment.py`:

Data/Raw/pilot_sample_raw.csv
Data/Raw/full_sample_raw.csv

**VI:** Dùng các file sample ở trên làm input cho LLM.

### 7.2 Use ground truth files only for evaluation

Use these files only for `compute_metric.py`:

Data/Raw/pilot_ground_truth_raw.csv
Data/Raw/full_ground_truth_raw.csv

**VI:** Chỉ dùng các file ground truth ở trên để đánh giá kết quả,
không dùng làm input cho LLM.

### 7.3 Recommended commands

Run the Raw pilot experiment:

.\.venv\Scripts\python.exe Scripts\run_experiment.py --version raw --phase pilot
.\.venv\Scripts\python.exe Scripts\compute_metric.py --version raw --phase pilot

Run the Raw full experiment:

.\.venv\Scripts\python.exe Scripts\run_experiment.py --version raw --phase full
.\.venv\Scripts\python.exe Scripts\compute_metric.py --version raw --phase full

---

## 8. Important Notes

- **EN:** Do not use `pilot_ground_truth_raw.csv` or
  `full_ground_truth_raw.csv` as LLM input because they contain manual labels
  and annotation information.
- **VI:** Không dùng `pilot_ground_truth_raw.csv` hoặc
  `full_ground_truth_raw.csv` làm input cho LLM vì các file này chứa nhãn
  thủ công và thông tin annotation.

- **EN:** Use `pilot_sample_raw.csv` and `full_sample_raw.csv` as the LLM
  input files.
- **VI:** Dùng `pilot_sample_raw.csv` và `full_sample_raw.csv` làm input
  cho LLM.

- **EN:** Raw reports contain the original bug report text before improvement.
- **VI:** Báo cáo Raw chứa nội dung bug report gốc trước khi được cải thiện.

- **EN:** The file `kappa_scores_raw.csv` is used to report inter-annotator
  agreement for the pilot annotation process.
- **VI:** File `kappa_scores_raw.csv` dùng để báo cáo độ đồng thuận giữa
  annotators trong giai đoạn pilot.

- **EN:** Result files generated by LLM experiments should be stored in
  `Results/Raw/`, not in `Data/Raw/`.
- **VI:** Các file kết quả do LLM tạo ra nên được lưu trong `Results/Raw/`,
  không lưu trong `Data/Raw/`.

---

## 9. Related Output Folder

The output files for Raw experiments are expected to be stored in:

Results/Raw/

Typical output files include:

pilot_llm_output_raw.csv
pilot_api_log_raw.csv
summary_raw.csv
mismatch_analysis_raw.csv

full_llm_output_raw.csv
full_api_log_raw.csv
summary_full_raw.csv
mismatch_analysis_full_raw.csv

**VI:** Các file kết quả của thí nghiệm Raw nên được lưu tại `Results/Raw/`.

---

## 10. Scope

This README only describes the `Data/Raw/` folder.

It does not cover:

- `Data/Improved/`
- `Results/`
- `Figures/`
- analysis notebooks such as `pilot_analysis.ipynb` or `full_analysis.ipynb`

**VI:** README này chỉ mô tả thư mục `Data/Raw/`. README này không mô tả
`Data/Improved/`, `Results/`, `Figures/`, hoặc các notebook phân tích.
