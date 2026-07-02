# Project Notes / Ghi chú dự án

## 1. Current Project Status / Trạng thái hiện tại của dự án

English:

The project structure has been completed for both Raw and Improved datasets. The project can now prepare data, run LLM experiments, compute metrics, compare Raw and Improved results, and recreate clean analysis notebooks.

Tiếng Việt:

Cấu trúc project đã được hoàn thiện cho cả hai bộ dữ liệu Raw và Improved. Project hiện có thể chuẩn bị dữ liệu, chạy thí nghiệm LLM, tính metric, so sánh Raw và Improved, và tạo lại notebook phân tích sạch.

Main comparison / So sánh chính:

Raw bug reports vs Improved bug reports
Bug report gốc so với bug report đã được cải thiện

Current status / Trạng thái hiện tại:

Data preparation              : DONE
Raw pilot experiment           : DONE
Improved pilot experiment      : DONE
Raw full experiment            : DONE
Improved full experiment       : DONE
Raw vs Improved comparison     : DONE
Analysis notebook preparation  : DONE

---

## 2. Research Context / Bối cảnh nghiên cứu

English:

The research topic focuses on automatic bug report quality assessment using large language models. The main quality criterion in this project is reproducibility, especially whether a bug report contains enough information for the Steps to Reproduce to be executable.

Tiếng Việt:

Chủ đề nghiên cứu tập trung vào việc đánh giá chất lượng bug report tự động bằng mô hình ngôn ngữ lớn. Tiêu chí chất lượng chính trong project là reproducibility, đặc biệt là việc bug report có đủ thông tin để Steps to Reproduce có thể thực hiện được hay không.

Research question / Câu hỏi nghiên cứu:

For bug reports on Mojira / Minecraft Issue Tracker, can an LLM automatically assess bug report quality based on reproducibility criteria, compared with human manual review, and achieve Cohen's Kappa >= 0.70?

Đối với các báo cáo lỗi trên Mojira / Minecraft Issue Tracker, LLM có thể tự động đánh giá chất lượng bug report theo tiêu chí reproducibility, so với đánh giá thủ công của con người, và đạt Cohen's Kappa >= 0.70 hay không?

Main metric / Chỉ số đánh giá chính:

Cohen's Kappa

Research threshold / Ngưỡng nghiên cứu:

Cohen's Kappa >= 0.70

---

## 3. Dataset Source / Nguồn dữ liệu

English:

The dataset is based on the ImproBR Replication Package. The dataset domain is Mojira / Minecraft Issue Tracker bug reports.

Tiếng Việt:

Bộ dữ liệu được lấy dựa trên ImproBR Replication Package. Miền dữ liệu là các bug report từ Mojira / Minecraft Issue Tracker.

Dataset information / Thông tin bộ dữ liệu:

Original source : ImproBR Replication Package
Platform        : Figshare
Domain          : Mojira / Minecraft Issue Tracker bug reports
Source page     : [Figshare source page](https://figshare.com/articles/software/ImproBR_Replication_Package/30086083)

License note / Ghi chú giấy phép:

The dataset license should be verified from the original Figshare package or the original README file.
Giấy phép của bộ dữ liệu cần được kiểm tra lại từ package gốc trên Figshare hoặc README gốc của package.

---

## 4. Root Files / Các file ở thư mục gốc

English:

The project root contains basic repository files for Git tracking, licensing, and project notes.

Tiếng Việt:

Thư mục gốc của project chứa các file cơ bản phục vụ Git, giấy phép, và ghi chú dự án.

Current root files / Các file hiện tại:

.gitignore
LICENSE
Notes.md

### 4.1 .gitignore

English:

The `.gitignore` file prevents sensitive or generated local files from being committed to Git.

Tiếng Việt:

File `.gitignore` giúp tránh commit các file nhạy cảm hoặc file cục bộ được sinh ra trong quá trình chạy project.

Current ignored items / Các mục đang được ignore:

.env
.vscode/
.venv/
__pycache__/
*.pyc

### 4.2 LICENSE

English:

The `LICENSE` file stores the project license information.

Tiếng Việt:

File `LICENSE` lưu thông tin giấy phép của project.

### 4.3 Notes.md

English:

The `Notes.md` file records the current project status, folder structure, experiment results, and next steps.

Tiếng Việt:

File `Notes.md` ghi lại trạng thái hiện tại của project, cấu trúc thư mục, kết quả thí nghiệm, và các bước tiếp theo.

---

## 5. Data Folder Structure / Cấu trúc thư mục Data

English:

The `Data/` folder is organized into three main parts: Annotations, Raw, and Improved.

Tiếng Việt:

Thư mục `Data/` được tổ chức thành ba phần chính: Annotations, Raw, và Improved.

Current structure / Cấu trúc hiện tại:

Data/
├── Annotations/
├── Raw/
└── Improved/

---

## 6. Data/Annotations

English:

This folder stores the original annotation source files. These files are used to derive ground truth files for both Raw and Improved datasets.

Tiếng Việt:

Thư mục này lưu các file annotation gốc. Các file này được dùng để tạo ground truth cho cả hai bộ dữ liệu Raw và Improved.

Current files / Các file hiện tại:

Data/Annotations/
├── Author 1 Responses.csv
├── Author 2 Responses.csv
└── Final Results.csv

Main purpose / Mục đích chính:

Data/Annotations/Final Results.csv is used to generate full ground truth files for both Raw and Improved datasets.

Data/Annotations/Final Results.csv được dùng để tạo các file full ground truth cho cả bộ dữ liệu Raw và Improved.

Important rule / Quy tắc quan trọng:

Do not manually edit annotation labels unless there is a documented correction.
Không tự ý chỉnh sửa nhãn annotation nếu không có ghi chú chỉnh sửa rõ ràng.

---

## 7. Data/Raw

English:

This folder stores the Raw version of the dataset. The Raw dataset represents the original bug reports before improvement. It is used as the baseline for comparison with the Improved dataset.

Tiếng Việt:

Thư mục này lưu phiên bản Raw của bộ dữ liệu. Dữ liệu Raw là các bug report gốc trước khi được cải thiện. Bộ dữ liệu này được dùng làm baseline để so sánh với bộ dữ liệu Improved.

Current files / Các file hiện tại:

Data/Raw/
├── RAW/
├── README.md
├── full_ground_truth_raw.csv
├── full_sample_raw.csv
├── kappa_scores_raw.csv
├── pilot_annotation_raw_author1.csv
├── pilot_annotation_raw_author2.csv
├── pilot_ground_truth_raw.csv
└── pilot_sample_raw.csv

Raw dataset statistics / Thống kê bộ Raw:

Pilot cases                  : 26
Full cases                   : 139
Pilot ground truth Executable     : 10
Pilot ground truth Non-Executable : 16
Full ground truth Executable      : 40
Full ground truth Non-Executable  : 99
Pilot Cohen Kappa between authors : 0.7647
Pilot agreement                  : 22/26

Conclusion / Kết luận:

Data/Raw is valid and ready for Raw-side LLM experiments.
Data/Raw hợp lệ và đã sẵn sàng cho thí nghiệm LLM phía Raw.

---

## 8. Data/Improved

English:

This folder stores the Improved version of the dataset. The Improved dataset represents bug reports after quality improvement, especially for Steps to Reproduce, Observed Behavior, Expected Behavior, and Environment.

Tiếng Việt:

Thư mục này lưu phiên bản Improved của bộ dữ liệu. Dữ liệu Improved là các bug report sau khi đã được cải thiện chất lượng, đặc biệt ở phần Steps to Reproduce, Observed Behavior, Expected Behavior, và Environment.

Current files / Các file hiện tại:

Data/Improved/
├── IMPROVED/
├── README.md
├── full_ground_truth_improved.csv
├── full_sample_improved.csv
├── kappa_scores_improved.csv
├── pilot_annotation_improved_author1.csv
├── pilot_annotation_improved_author2.csv
├── pilot_ground_truth_improved.csv
└── pilot_sample_improved.csv

Improved dataset statistics / Thống kê bộ Improved:

Pilot cases                  : 26
Full cases                   : 139
Pilot ground truth Executable     : 19
Pilot ground truth Non-Executable : 7
Full ground truth Executable      : 94
Full ground truth Non-Executable  : 45
Pilot Cohen Kappa between authors : 0.7524
Pilot agreement                  : 22/26

Conclusion / Kết luận:

Data/Improved is valid and ready for Improved-side LLM experiments.
Data/Improved hợp lệ và đã sẵn sàng cho thí nghiệm LLM phía Improved.

---

## 9. Scripts Folder Structure / Cấu trúc thư mục Scripts

English:

The `Scripts/` folder contains the execution scripts for data checking, data preparation, LLM experiments, metric computation, result comparison, and notebook recreation.

Tiếng Việt:

Thư mục `Scripts/` chứa các script thực thi để kiểm tra dữ liệu, chuẩn bị dữ liệu, chạy thí nghiệm LLM, tính metric, so sánh kết quả, và tạo lại notebook.

Current structure / Cấu trúc hiện tại:

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

Main workflow / Quy trình chính:

Generate pilot data
-> Compute pilot kappa
-> Create full ground truth
-> Create full sample files
-> Test API
-> Run LLM experiment
-> Compute metrics
-> Compare Raw vs Improved
-> Recreate clean notebooks if needed

---

## 10. Results Folder Structure / Cấu trúc thư mục Results

English:

The `Results/` folder stores LLM outputs, API logs, summary metrics, mismatch analysis files, comparison files, and analysis notebooks.

Tiếng Việt:

Thư mục `Results/` lưu output của LLM, log API, summary metric, file phân tích mismatch, file so sánh, và notebook phân tích.

Current structure / Cấu trúc hiện tại:

Results/
├── Raw/
│   ├── README.md
│   ├── .gitkeep
│   ├── pilot_llm_output_raw.csv
│   ├── pilot_api_log_raw.csv
│   ├── summary_raw.csv
│   ├── mismatch_analysis_raw.csv
│   ├── full_llm_output_raw.csv
│   ├── full_api_log_raw.csv
│   ├── summary_full_raw.csv
│   └── mismatch_analysis_full_raw.csv
│
├── Improved/
│   ├── README.md
│   ├── .gitkeep
│   ├── pilot_llm_output_improved.csv
│   ├── pilot_api_log_improved.csv
│   ├── summary_improved.csv
│   ├── mismatch_analysis_improved.csv
│   ├── full_llm_output_improved.csv
│   ├── full_api_log_improved.csv
│   ├── summary_full_improved.csv
│   └── mismatch_analysis_full_improved.csv
│
├── comparison_raw_vs_improved_pilot.csv
├── comparison_raw_vs_improved_full.csv
├── pilot_analysis.ipynb
├── full_analysis.ipynb
└── summary.csv

Important update / Cập nhật quan trọng:

The result files are no longer pending.
Các file kết quả không còn ở trạng thái pending.

---

## 11. Pilot Experiment Results / Kết quả thí nghiệm Pilot

### 11.1 Raw Pilot

English:

The Raw pilot experiment was completed and evaluated.

Tiếng Việt:

Thí nghiệm pilot của Raw đã được chạy và đánh giá.

Result / Kết quả:

Total cases      : 26
Accuracy         : 0.6923
Cohen Kappa      : 0.3247
Threshold        : 0.70
Threshold passed : False
Mismatch cases   : 8

### 11.2 Improved Pilot

English:

The Improved pilot experiment was completed and evaluated.

Tiếng Việt:

Thí nghiệm pilot của Improved đã được chạy và đánh giá.

Result / Kết quả:
Total cases      : 26
Accuracy         : 0.7308
Cohen Kappa      : 0.0000
Threshold        : 0.70
Threshold passed : False
Mismatch cases   : 7

Pilot conclusion / Kết luận pilot:

Both Raw and Improved pilot results did not reach the target Cohen Kappa threshold of 0.70.

Cả Raw và Improved ở pilot đều chưa đạt ngưỡng Cohen Kappa mục tiêu là 0.70.

---

## 12. Full Experiment Results / Kết quả thí nghiệm Full

### 12.1 Raw Full

English:

The Raw full experiment was completed and evaluated.

Tiếng Việt:

Thí nghiệm full của Raw đã được chạy và đánh giá.

Result / Kết quả:

Total cases       : 139
Correct           : 102
Incorrect         : 37
Accuracy          : 0.7338
Cohen Kappa       : 0.3358
Threshold         : 0.70
Threshold passed  : False
Total cost USD    : 0.01809390

Confusion matrix / Ma trận nhầm lẫn:

Ground Truth Executable     -> LLM Executable     : 20
Ground Truth Executable     -> LLM Non-Executable : 20
Ground Truth Non-Executable -> LLM Executable     : 17
Ground Truth Non-Executable -> LLM Non-Executable : 82

### 12.2 Improved Full

English:

The Improved full experiment was completed and evaluated.

Tiếng Việt:

Thí nghiệm full của Improved đã được chạy và đánh giá.

Result / Kết quả:

Total cases       : 139
Correct           : 96
Incorrect         : 43
Accuracy          : 0.6906
Cohen Kappa       : 0.0592
Threshold         : 0.70
Threshold passed  : False
Total cost USD    : 0.02465280

Confusion matrix / Ma trận nhầm lẫn:

Ground Truth Executable     -> LLM Executable     : 94
Ground Truth Executable     -> LLM Non-Executable : 0
Ground Truth Non-Executable -> LLM Executable     : 43
Ground Truth Non-Executable -> LLM Non-Executable : 2

Full conclusion / Kết luận full:

Both Raw and Improved full results did not reach the target Cohen Kappa threshold of 0.70.

Cả Raw và Improved ở full đều chưa đạt ngưỡng Cohen Kappa mục tiêu là 0.70.

---

## 13. Raw vs Improved Comparison / So sánh Raw và Improved

English:

The Raw full experiment outperformed the Improved full experiment in both Accuracy and Cohen's Kappa.

Tiếng Việt:

Thí nghiệm full của Raw có kết quả tốt hơn Improved ở cả Accuracy và Cohen's Kappa.

Full comparison / So sánh full:

Raw Accuracy       : 0.7338
Improved Accuracy  : 0.6906
Raw Cohen Kappa    : 0.3358
Improved Kappa     : 0.0592
Raw cost USD       : 0.01809390
Improved cost USD  : 0.02465280

Interpretation / Diễn giải:

Although the Improved reports contain more structured information, the LLM showed a strong bias toward classifying Improved reports as Executable. This reduced Cohen's Kappa.

Mặc dù báo cáo Improved có nhiều thông tin được cấu trúc hơn, LLM có xu hướng mạnh khi phân loại Improved thành Executable. Điều này làm Cohen's Kappa giảm mạnh.

---

## 14. Statistical Analysis Notebook / Notebook phân tích thống kê

English:

The `full_analysis.ipynb` notebook follows the required statistical analysis workflow.

Tiếng Việt:

Notebook `full_analysis.ipynb` làm theo workflow phân tích thống kê được yêu cầu.

Required workflow / Quy trình yêu cầu:

1. Compute metrics on the complete output.
2. Run the selected statistical test from the proposal with alpha = 0.05.
3. Compute effect size.
4. Write results to Results/summary.csv with metric value, p-value, effect size, and N.
5. Conclude each research question using reject H0 or fail to reject H0.

Selected statistical test / Kiểm định thống kê được chọn:

McNemar exact test

Reason / Lý do:

Raw and Improved predictions are paired by the same issue keys.
Dự đoán Raw và Improved là dữ liệu cặp theo cùng issue key.

Effect size / Kích thước ảnh hưởng:

Cliff's delta

Effect size interpretation / Diễn giải effect size:

small / nhỏ       : absolute delta < 0.2
medium / trung bình : 0.2 <= absolute delta <= 0.5
large / lớn       : absolute delta > 0.5

Important rule / Quy tắc quan trọng:

Do not change the statistical test after looking at the data to get a better result.
Không đổi statistical test sau khi xem data để tạo kết quả đẹp hơn.

---

## 15. Analysis Notebooks / Notebook phân tích

English:

The analysis notebooks are stored in `Results/` and are generated by `Scripts/recreate_clean_analysis_notebooks.py`.

Tiếng Việt:

Các notebook phân tích được lưu trong `Results/` và được tạo bởi `Scripts/recreate_clean_analysis_notebooks.py`.

Notebook files / Các file notebook:

Results/pilot_analysis.ipynb
Results/full_analysis.ipynb

Notebook design / Thiết kế notebook:

Bilingual English and Vietnamese markdown
No pandas
No matplotlib
No statsmodels
Uses only Python built-in libraries
Writes Results/summary.csv from full_analysis.ipynb

Verification command / Lệnh kiểm tra:

Select-String -Path ".\Results\pilot_analysis.ipynb",".\Results\full_analysis.ipynb" -Pattern "statsmodels|matplotlib|pandas"

Expected result / Kết quả mong đợi:

No output

---

## 16. Results Summary CSV / File Results/summary.csv

English:

The file `Results/summary.csv` is generated by `full_analysis.ipynb`.

Tiếng Việt:

File `Results/summary.csv` được tạo bởi `full_analysis.ipynb`.

Expected columns / Các cột mong đợi:

metric
value
p_value
effect_size
N
alpha
decision
interpretation

Purpose / Mục đích:

This file records metric value, p-value, effect size, sample size, alpha, decision, and interpretation for the full analysis.

File này ghi lại metric value, p-value, effect size, cỡ mẫu, alpha, quyết định kiểm định, và diễn giải cho phân tích full.

---

## 17. Commands / Các lệnh chạy chính

### 17.1 Generate pilot files / Tạo file pilot

.\.venv\Scripts\python.exe Scripts\generate_pilot.py

### 17.2 Compute pilot kappa / Tính kappa pilot

.\.venv\Scripts\python.exe Scripts\kappa_pilot.py

### 17.3 Create full ground truth / Tạo full ground truth

.\.venv\Scripts\python.exe Scripts\Raw\create_full_ground_truth_raw.py
.\.venv\Scripts\python.exe Scripts\Improved\create_full_ground_truth_improved.py

### 17.4 Create full samples / Tạo full sample

.\.venv\Scripts\python.exe Scripts\create_full_samples.py

### 17.5 Test API / Kiểm tra API

.\.venv\Scripts\python.exe Scripts\test_api.py --version raw
.\.venv\Scripts\python.exe Scripts\test_api.py --version improved

### 17.6 Run pilot experiments / Chạy thí nghiệm pilot

.\.venv\Scripts\python.exe Scripts\run_experiment.py --version raw --phase pilot
.\.venv\Scripts\python.exe Scripts\compute_metric.py --version raw --phase pilot

.\.venv\Scripts\python.exe Scripts\run_experiment.py --version improved --phase pilot
.\.venv\Scripts\python.exe Scripts\compute_metric.py --version improved --phase pilot

.\.venv\Scripts\python.exe Scripts\compare_raw_improved.py --phase pilot

### 17.7 Run full experiments / Chạy thí nghiệm full

.\.venv\Scripts\python.exe Scripts\run_experiment.py --version raw --phase full
.\.venv\Scripts\python.exe Scripts\compute_metric.py --version raw --phase full

.\.venv\Scripts\python.exe Scripts\run_experiment.py --version improved --phase full
.\.venv\Scripts\python.exe Scripts\compute_metric.py --version improved --phase full

.\.venv\Scripts\python.exe Scripts\compare_raw_improved.py --phase full

### 17.8 Recreate analysis notebooks / Tạo lại notebook phân tích

.\.venv\Scripts\python.exe Scripts\recreate_clean_analysis_notebooks.py

---

## 18. Important Notes / Ghi chú quan trọng

English:

Do not use ground truth files as LLM input.

Tiếng Việt:

Không dùng file ground truth làm input cho LLM.

English:

Use sample files as LLM input.

Tiếng Việt:

Dùng các file sample làm input cho LLM.

English:

Run `compute_metric.py` only after `run_experiment.py`.

Tiếng Việt:

Chỉ chạy `compute_metric.py` sau khi đã chạy `run_experiment.py`.

English:

Run `compare_raw_improved.py` only after both Raw and Improved summary files exist.

Tiếng Việt:

Chỉ chạy `compare_raw_improved.py` sau khi summary của cả Raw và Improved đã tồn tại.

English:

Do not change the statistical test after looking at the result.

Tiếng Việt:

Không đổi kiểm định thống kê sau khi xem kết quả.

English:

Keep `Figures/` unchanged unless your role explicitly requires editing it.

Tiếng Việt:

Không chỉnh sửa `Figures/` trừ khi vai trò của bạn yêu cầu rõ ràng.

---

## 19. Final Project Conclusion / Kết luận cuối của project

English:

The full experiment shows that the current LLM-based reproducibility classification setup did not reach the required agreement level with manual/developer review. Raw performed better than Improved in both Accuracy and Cohen's Kappa.

Tiếng Việt:

Kết quả full experiment cho thấy thiết lập phân loại khả năng tái hiện lỗi bằng LLM hiện tại chưa đạt mức đồng thuận yêu cầu với manual/developer review. Raw có kết quả tốt hơn Improved ở cả Accuracy và Cohen's Kappa.

Final conclusion / Kết luận cuối:

Raw Cohen Kappa      : 0.3358
Improved Cohen Kappa : 0.0592
Target threshold     : 0.70
Result               : Not achieved

English:

Therefore, the answer to the research question is that the current LLM setup does not achieve Cohen's Kappa >= 0.70.

Tiếng Việt:

Vì vậy, câu trả lời cho research question là thiết lập LLM hiện tại chưa đạt Cohen's Kappa >= 0.70.
