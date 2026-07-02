# Scripts README

> **EN:** This folder contains Python scripts for preparing data, running LLM experiments, computing metrics, comparing Raw and Improved results, checking project files, and recreating clean analysis notebooks.
>
> **VI:** Thư mục này chứa các script Python dùng để chuẩn bị dữ liệu, chạy thí nghiệm LLM, tính metric, so sánh Raw và Improved, kiểm tra file trong project, và tạo lại notebook phân tích sạch.

---

## 1. Purpose

**EN:** The `Scripts/` folder is the main execution layer of the project. It connects the dataset files in `Data/` with the generated outputs in `Results/`.

**VI:** Thư mục `Scripts/` là phần thực thi chính của project. Nó kết nối dữ liệu trong `Data/` với các kết quả được tạo ra trong `Results/`.

**EN:** The main workflow is:

**VI:** Quy trình chính là:

Check data
-> Create pilot files
-> Compute pilot inter-annotator agreement
-> Create full ground truth files
-> Create full sample files
-> Test API
-> Run LLM experiment
-> Compute evaluation metrics
-> Compare Raw vs Improved
-> Recreate clean analysis notebooks if needed

---

## 2. Current Folder Structure

**EN:** The current `Scripts/` folder is organized by dataset-specific helper scripts and general experiment scripts.

**VI:** Thư mục `Scripts/` hiện tại được tổ chức thành các script phụ theo từng bộ dữ liệu và các script thí nghiệm chung.

Scripts/
├── Improved/
│   ├── check_improved_data.py
│   └── create_full_ground_truth_improved.py
│
├── Raw/
│   ├── check_raw_data.py
│   └── create_full_ground_truth_raw.py
│
├── compare_raw_improved.py
├── compute_metric.py
├── create_full_samples.py
├── generate_pilot.py
├── kappa_pilot.py
├── README.md
├── recreate_clean_analysis_notebooks.py
├── run_experiment.py
└── test_api.py

---

## 3. Path Convention

### 3.1 Main scripts

**EN:** The main scripts are placed directly inside `Scripts/`. They resolve the project root from one level above the script folder.

**VI:** Các script chính được đặt trực tiếp trong `Scripts/`. Chúng xác định project root bằng cách đi lên một cấp từ thư mục script.

Main scripts:

Scripts/run_experiment.py
Scripts/compute_metric.py
Scripts/compare_raw_improved.py
Scripts/generate_pilot.py
Scripts/kappa_pilot.py
Scripts/create_full_samples.py
Scripts/test_api.py
Scripts/recreate_clean_analysis_notebooks.py

### 3.2 Raw and Improved helper scripts

**EN:** The Raw and Improved helper scripts are placed inside subfolders. Because they are one level deeper, they resolve the project root by going up two levels.

**VI:** Các script phụ của Raw và Improved được đặt trong thư mục con. Vì chúng nằm sâu hơn một cấp, chúng xác định project root bằng cách đi lên hai cấp.

Subfolder scripts:

Scripts/Raw/check_raw_data.py
Scripts/Raw/create_full_ground_truth_raw.py

Scripts/Improved/check_improved_data.py
Scripts/Improved/create_full_ground_truth_improved.py
Example path relationship:

SWT301_SE1925_G6/
└── Scripts/
    └── Raw/
        └── check_raw_data.py

For a script inside `Scripts/Raw/` or `Scripts/Improved/`:

Level 0: Scripts/Raw or Scripts/Improved
Level 1: Scripts
Level 2: SWT301_SE1925_G6

---

## 4. Raw Helper Scripts

### 4.1 Scripts/Raw/check_raw_data.py

**EN:** This script checks whether the required `Data/Raw/` files exist and validates Raw data consistency.

**VI:** Script này kiểm tra các file cần thiết trong `Data/Raw/` và kiểm tra tính nhất quán của dữ liệu Raw.

Files checked:

Data/Raw/full_ground_truth_raw.csv
Data/Raw/kappa_scores_raw.csv
Data/Raw/pilot_annotation_raw_author1.csv
Data/Raw/pilot_annotation_raw_author2.csv
Data/Raw/pilot_ground_truth_raw.csv
Data/Raw/pilot_sample_raw.csv

**EN:** It also checks the status of expected result files in `Results/Raw/`.

**VI:** Script này cũng kiểm tra trạng thái các file kết quả mong đợi trong `Results/Raw/`.

Run from project root:

.\.venv\Scripts\python.exe Scripts\Raw\check_raw_data.py

### 4.2 Scripts/Raw/create_full_ground_truth_raw.py

**EN:** This script creates the full Raw ground truth file from `Data/Annotations/Final Results.csv`.

**VI:** Script này tạo file ground truth full cho Raw từ `Data/Annotations/Final Results.csv`.

Input:

Data/Annotations/Final Results.csv

Output:

Data/Raw/full_ground_truth_raw.csv

Run from project root:

.\.venv\Scripts\python.exe Scripts\Raw\create_full_ground_truth_raw.py

---

## 5. Improved Helper Scripts

### 5.1 Scripts/Improved/check_improved_data.py

**EN:** This script checks whether the required `Data/Improved/` files exist and validates Improved data consistency.

**VI:** Script này kiểm tra các file cần thiết trong `Data/Improved/` và kiểm tra tính nhất quán của dữ liệu Improved.

Files checked:

Data/Improved/full_ground_truth_improved.csv
Data/Improved/kappa_scores_improved.csv
Data/Improved/pilot_annotation_improved_author1.csv
Data/Improved/pilot_annotation_improved_author2.csv
Data/Improved/pilot_ground_truth_improved.csv
Data/Improved/pilot_sample_improved.csv

**EN:** It also checks the status of expected result files in `Results/Improved/`.

**VI:** Script này cũng kiểm tra trạng thái các file kết quả mong đợi trong `Results/Improved/`.

Run from project root:

.\.venv\Scripts\python.exe Scripts\Improved\check_improved_data.py

### 5.2 Scripts/Improved/create_full_ground_truth_improved.py

**EN:** This script creates the full Improved ground truth file from `Data/Annotations/Final Results.csv`.

**VI:** Script này tạo file ground truth full cho Improved từ `Data/Annotations/Final Results.csv`.

Input:

Data/Annotations/Final Results.csv

Output:

Data/Improved/full_ground_truth_improved.csv

Run from project root:

.\.venv\Scripts\python.exe Scripts\Improved\create_full_ground_truth_improved.py

---

## 6. Pilot Data Scripts

### 6.1 generate_pilot.py

**EN:** This script generates pilot files for both Raw and Improved datasets.

**VI:** Script này tạo các file pilot cho cả hai bộ dữ liệu Raw và Improved.

Input:

Data/Raw/RAW/
Data/Improved/IMPROVED/
Data/Annotations/Author 1 Responses.csv
Data/Annotations/Author 2 Responses.csv
Data/Annotations/Final Results.csv

Output:

Data/Raw/pilot_sample_raw.csv
Data/Raw/pilot_ground_truth_raw.csv
Data/Raw/pilot_annotation_raw_author1.csv
Data/Raw/pilot_annotation_raw_author2.csv

Data/Improved/pilot_sample_improved.csv
Data/Improved/pilot_ground_truth_improved.csv
Data/Improved/pilot_annotation_improved_author1.csv
Data/Improved/pilot_annotation_improved_author2.csv

Run from project root:

.\.venv\Scripts\python.exe Scripts\generate_pilot.py

Important note:

This script overwrites existing pilot files.
Do not run it again after LLM results have already been generated unless you intentionally want to regenerate the pilot sample.

**VI:** Script này sẽ ghi đè các file pilot hiện có. Không nên chạy lại sau khi đã có kết quả LLM, trừ khi muốn tạo lại pilot sample.

### 6.2 kappa_pilot.py

**EN:** This script computes Cohen's Kappa and Inter-Annotator Agreement for pilot Raw and Improved annotations.

**VI:** Script này tính Cohen's Kappa và độ đồng thuận giữa annotators cho pilot Raw và Improved.

Input:

Data/Raw/pilot_ground_truth_raw.csv
Data/Raw/pilot_annotation_raw_author1.csv
Data/Raw/pilot_annotation_raw_author2.csv

Data/Improved/pilot_ground_truth_improved.csv
Data/Improved/pilot_annotation_improved_author1.csv
Data/Improved/pilot_annotation_improved_author2.csv

Output:

Data/Raw/kappa_scores_raw.csv
Data/Improved/kappa_scores_improved.csv

Run from project root:

.\.venv\Scripts\python.exe Scripts\kappa_pilot.py

---

## 7. Full Data Preparation Script

### 7.1 create_full_samples.py

**EN:** This script creates full LLM input sample files for Raw and Improved datasets.

**VI:** Script này tạo file input full cho LLM đối với cả Raw và Improved.

**EN:** Ground truth files contain labels and must not be used as LLM input. This script creates separate `full_sample_*.csv` files that contain only bug report content for `run_experiment.py`.

**VI:** Các file ground truth có chứa nhãn nên không được dùng làm input cho LLM. Script này tạo các file `full_sample_*.csv` riêng, chỉ chứa nội dung bug report để đưa vào `run_experiment.py`.

Input:

Data/Raw/RAW/
Data/Improved/IMPROVED/
Data/Raw/full_ground_truth_raw.csv
Data/Improved/full_ground_truth_improved.csv

Output:

Data/Raw/full_sample_raw.csv
Data/Improved/full_sample_improved.csv

Run from project root:

.\.venv\Scripts\python.exe Scripts\create_full_samples.py

Important note:

This script overwrites existing full_sample_raw.csv and full_sample_improved.csv.

**VI:** Script này sẽ ghi đè `full_sample_raw.csv` và `full_sample_improved.csv` nếu các file này đã tồn tại.

---

## 8. LLM API Scripts

### 8.1 test_api.py

**EN:** This script sends one test request to the OpenAI API using one pilot sample row.

**VI:** Script này gửi một request thử đến OpenAI API bằng một dòng pilot sample.

Use this script before running the experiment to confirm:

.env is loaded correctly
OPENAI_API_KEY exists
openai package is installed
model can return valid JSON
cost calculation works

**VI:** Nên dùng script này trước khi chạy thí nghiệm để kiểm tra API key, package OpenAI, JSON output, và tính cost.

Run Raw test:

.\.venv\Scripts\python.exe Scripts\test_api.py --version raw

Run Improved test:

.\.venv\Scripts\python.exe Scripts\test_api.py --version improved

### 8.2 run_experiment.py

**EN:** This script runs the LLM reproducibility classification experiment.

**VI:** Script này chạy thí nghiệm phân loại khả năng tái hiện lỗi bằng LLM.

Supported dataset versions:

raw
improved

Supported phases:

pilot
full

Run Raw pilot:

.\.venv\Scripts\python.exe Scripts\run_experiment.py --version raw --phase pilot

Run Improved pilot:

.\.venv\Scripts\python.exe Scripts\run_experiment.py --version improved --phase pilot

Run Raw full:

.\.venv\Scripts\python.exe Scripts\run_experiment.py --version raw --phase full

Run Improved full:

.\.venv\Scripts\python.exe Scripts\run_experiment.py --version improved --phase full

Output examples:

Results/Raw/pilot_llm_output_raw.csv
Results/Raw/pilot_api_log_raw.csv
Results/Raw/full_llm_output_raw.csv
Results/Raw/full_api_log_raw.csv

Results/Improved/pilot_llm_output_improved.csv
Results/Improved/pilot_api_log_improved.csv
Results/Improved/full_llm_output_improved.csv
Results/Improved/full_api_log_improved.csv

---

## 9. Evaluation Scripts

### 9.1 compute_metric.py

**EN:** This script computes evaluation metrics by comparing LLM predictions with manual ground truth labels.

**VI:** Script này tính các metric đánh giá bằng cách so sánh dự đoán của LLM với nhãn ground truth thủ công.

Metrics include:

Accuracy
Cohen Kappa
Threshold passed
Confusion matrix
Missing predictions
Extra predictions
Token usage
Total cost USD
Mismatch analysis

Run Raw pilot metric:

.\.venv\Scripts\python.exe Scripts\compute_metric.py --version raw --phase pilot

Run Improved pilot metric:

.\.venv\Scripts\python.exe Scripts\compute_metric.py --version improved --phase pilot

Run Raw full metric:

.\.venv\Scripts\python.exe Scripts\compute_metric.py --version raw --phase full

Run Improved full metric:

.\.venv\Scripts\python.exe Scripts\compute_metric.py --version improved --phase full

Output examples:

Results/Raw/summary_raw.csv
Results/Raw/mismatch_analysis_raw.csv
Results/Raw/summary_full_raw.csv
Results/Raw/mismatch_analysis_full_raw.csv

Results/Improved/summary_improved.csv
Results/Improved/mismatch_analysis_improved.csv
Results/Improved/summary_full_improved.csv
Results/Improved/mismatch_analysis_full_improved.csv

### 9.2 compare_raw_improved.py

**EN:** This script compares Raw and Improved summary metrics for the same phase.

**VI:** Script này so sánh các metric summary giữa Raw và Improved trong cùng một phase.

Run pilot comparison:

.\.venv\Scripts\python.exe Scripts\compare_raw_improved.py --phase pilot

Run full comparison:

.\.venv\Scripts\python.exe Scripts\compare_raw_improved.py --phase full

Output:

Results/comparison_raw_vs_improved_pilot.csv
Results/comparison_raw_vs_improved_full.csv

---

## 10. Analysis Notebook Utility

### 10.1 recreate_clean_analysis_notebooks.py

**EN:** This script recreates clean analysis notebooks in `Results/` without external packages such as `pandas`, `matplotlib`, or `statsmodels`.

**VI:** Script này tạo lại notebook phân tích sạch trong `Results/` mà không cần các package ngoài như `pandas`, `matplotlib`, hoặc `statsmodels`.

This script writes:

Results/pilot_analysis.ipynb
Results/full_analysis.ipynb

Run from project root:

.\.venv\Scripts\python.exe Scripts\recreate_clean_analysis_notebooks.py

Verify that old imports are removed:

Select-String -Path ".\Results\pilot_analysis.ipynb",".\Results\full_analysis.ipynb" -Pattern "statsmodels|matplotlib|pandas"

Expected result:

No output

**VI:** Nếu không có output nào được in ra, notebook đã sạch.

---

## 11. Recommended Execution Order

### 11.1 Prepare pilot data

**EN:** Generate pilot sample, ground truth, author annotations, and pilot kappa scores.

**VI:** Tạo pilot sample, ground truth, annotation của authors, và điểm kappa pilot.

.\.venv\Scripts\python.exe Scripts\generate_pilot.py
.\.venv\Scripts\python.exe Scripts\kappa_pilot.py

### 11.2 Prepare full data

**EN:** Create full ground truth files and full LLM sample files.

**VI:** Tạo file full ground truth và file full sample dùng cho LLM.

.\.venv\Scripts\python.exe Scripts\Raw\create_full_ground_truth_raw.py
.\.venv\Scripts\python.exe Scripts\Improved\create_full_ground_truth_improved.py
.\.venv\Scripts\python.exe Scripts\create_full_samples.py

### 11.3 Validate data

**EN:** Check whether required Raw and Improved files exist and whether their issue keys are consistent.

**VI:** Kiểm tra các file Raw và Improved cần thiết, đồng thời kiểm tra issue key có nhất quán không.

.\.venv\Scripts\python.exe Scripts\Raw\check_raw_data.py
.\.venv\Scripts\python.exe Scripts\Improved\check_improved_data.py

### 11.4 Test API

**EN:** Test one Raw request and one Improved request before running the full experiment.

**VI:** Test một request Raw và một request Improved trước khi chạy thí nghiệm đầy đủ.

.\.venv\Scripts\python.exe Scripts\test_api.py --version raw
.\.venv\Scripts\python.exe Scripts\test_api.py --version improved

### 11.5 Run pilot experiment

**EN:** Run pilot LLM prediction, compute pilot metrics, and compare Raw vs Improved.

**VI:** Chạy dự đoán LLM ở pilot, tính metric pilot, và so sánh Raw với Improved.

.\.venv\Scripts\python.exe Scripts\run_experiment.py --version raw --phase pilot
.\.venv\Scripts\python.exe Scripts\compute_metric.py --version raw --phase pilot

.\.venv\Scripts\python.exe Scripts\run_experiment.py --version improved --phase pilot
.\.venv\Scripts\python.exe Scripts\compute_metric.py --version improved --phase pilot

.\.venv\Scripts\python.exe Scripts\compare_raw_improved.py --phase pilot

### 11.6 Run full experiment

**EN:** Run full LLM prediction, compute full metrics, and compare Raw vs Improved.

**VI:** Chạy dự đoán LLM ở full, tính metric full, và so sánh Raw với Improved.

.\.venv\Scripts\python.exe Scripts\run_experiment.py --version raw --phase full
.\.venv\Scripts\python.exe Scripts\compute_metric.py --version raw --phase full

.\.venv\Scripts\python.exe Scripts\run_experiment.py --version improved --phase full
.\.venv\Scripts\python.exe Scripts\compute_metric.py --version improved --phase full

.\.venv\Scripts\python.exe Scripts\compare_raw_improved.py --phase full

### 11.7 Recreate clean notebooks if needed

**EN:** Use this only when `pilot_analysis.ipynb` or `full_analysis.ipynb` still contains old imports.

**VI:** Chỉ dùng bước này khi `pilot_analysis.ipynb` hoặc `full_analysis.ipynb` vẫn còn import cũ.

.\.venv\Scripts\python.exe Scripts\recreate_clean_analysis_notebooks.py

---

## 12. Environment Requirements

**EN:** Activate the virtual environment before running scripts.

**VI:** Kích hoạt virtual environment trước khi chạy script.

.\.venv\Scripts\activate

**EN:** Install the required OpenAI package.

**VI:** Cài package OpenAI cần thiết.

pip install openai

**EN:** Only these scripts require the OpenAI package:

**VI:** Chỉ các script sau cần package OpenAI:

test_api.py
run_experiment.py

**EN:** Most other scripts use Python built-in libraries.

**VI:** Phần lớn script còn lại dùng thư viện có sẵn của Python.

argparse
collections
csv
json
math
pathlib
random
time
typing

---

## 13. Environment Variables

**EN:** Create a `.env` file at the project root.

**VI:** Tạo file `.env` tại project root.

OPENAI_API_KEY=your_api_key_here

**EN:** The API scripts read `.env` from the project root.

**VI:** Các script gọi API sẽ đọc `.env` từ project root.

Important:

Do not commit .env to Git.

**VI:** Không commit file `.env` lên Git.

---

## 14. Important Notes

**EN:** Do not use ground truth files as LLM input.

**VI:** Không dùng file ground truth làm input cho LLM.

**EN:** Use sample files as LLM input.

**VI:** Dùng các file sample làm input cho LLM.

**EN:** Run `compute_metric.py` only after `run_experiment.py`.

**VI:** Chỉ chạy `compute_metric.py` sau khi đã chạy `run_experiment.py`.

**EN:** Run `compare_raw_improved.py` only after both Raw and Improved summary files exist.

**VI:** Chỉ chạy `compare_raw_improved.py` sau khi summary của cả Raw và Improved đã tồn tại.

**EN:** Be careful with scripts that overwrite generated files.

**VI:** Cẩn thận với các script có chức năng ghi đè file đã tạo.

**EN:** Keep `Figures/` unchanged unless your role explicitly requires editing it.

**VI:** Không chỉnh sửa `Figures/` trừ khi vai trò của bạn yêu cầu rõ ràng.

**EN:** If VS Code still reports old notebook import errors, run `recreate_clean_analysis_notebooks.py`.

**VI:** Nếu VS Code vẫn báo lỗi import cũ trong notebook, hãy chạy `recreate_clean_analysis_notebooks.py`.

---

## 15. Scope

**EN:** This README describes only the `Scripts/` folder.

**VI:** README này chỉ mô tả thư mục `Scripts/`.

It does not describe:

Data/Raw/
Data/Improved/
Results/Raw/
Results/Improved/
Figures/
