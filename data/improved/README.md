# Data/Improved README / Tài liệu thư mục Data/Improved

## 1. Overview / Tổng quan

**English:**  
This folder stores the **Improved** version of the Mojira bug report dataset used in the research project **Bug Report Quality Assessment with LLM**. The Improved dataset contains bug reports after improvement/refinement and is used to evaluate whether an LLM can assess bug report quality, especially **reproducibility**, consistently with human/manual review.

**Tiếng Việt:**  
Thư mục này lưu phiên bản dữ liệu **Improved** của các bug report trên Mojira, được sử dụng trong đề tài **Bug Report Quality Assessment with LLM**. Bộ dữ liệu Improved là phiên bản báo cáo lỗi đã được cải thiện/chỉnh sửa, dùng để đánh giá xem LLM có thể tự động đánh giá chất lượng bug report, đặc biệt là tiêu chí **reproducibility / khả năng tái hiện lỗi**, nhất quán với đánh giá thủ công của con người hay không.

---

## 2. Research Question / Câu hỏi nghiên cứu

**English:**  
For bug reports on Mojira / Minecraft Issue Tracker, can an LLM automatically assess bug report quality based on reproducibility compared with manual review, achieving **Cohen's Kappa ≥ 0.70**?

**Tiếng Việt:**  
Đối với các báo cáo lỗi trên Mojira / Minecraft Issue Tracker, LLM đánh giá chất lượng báo cáo lỗi tự động theo tiêu chí reproducibility so với đánh giá thủ công có đạt **Cohen's Kappa ≥ 0.70** hay không?

---

## 3. Folder Structure / Cấu trúc thư mục

Data/Improved/  
├── IMPROVED/  
│   └── Original or extracted improved dataset files  
├── full_ground_truth_improved.csv  
├── full_sample_improved.csv  
├── kappa_scores_improved.csv  
├── pilot_annotation_improved_author1.csv  
├── pilot_annotation_improved_author2.csv  
├── pilot_ground_truth_improved.csv  
├── pilot_sample_improved.csv  
└── README.md  

**English:**  
The `Data/Improved` folder is for storing improved input data, annotation files, and ground-truth files only. Generated LLM outputs, API logs, metric summaries, and mismatch analyses should be stored in `Results/Improved`, not in this folder.

**Tiếng Việt:**  
Thư mục `Data/Improved` chỉ dùng để lưu dữ liệu đầu vào đã cải thiện, file annotation và file ground truth. Các kết quả sinh ra từ LLM, API log, file summary metric và mismatch analysis nên được lưu trong `Results/Improved`, không lưu trực tiếp trong thư mục này.

---

## 4. File Inventory / Danh sách file dữ liệu

| File | Rows / Số dòng | English Description | Mô tả tiếng Việt |
| --- | ---: | --- | --- |
| `full_sample_improved.csv` | 139 | Full improved bug report sample used as the main LLM input for the full evaluation phase. | Bộ sample Improved đầy đủ, dùng làm dữ liệu đầu vào chính cho LLM ở giai đoạn full evaluation. |
| `full_ground_truth_improved.csv` | 139 | Ground-truth labels for the full improved dataset. Used to compare against LLM predictions. | Nhãn ground truth cho toàn bộ dữ liệu Improved, dùng để so sánh với kết quả dự đoán của LLM. |
| `pilot_sample_improved.csv` | 26 | Pilot subset of improved bug reports used for testing the workflow before the full run. | Tập pilot của dữ liệu Improved, dùng để kiểm thử quy trình trước khi chạy toàn bộ. |
| `pilot_annotation_improved_author1.csv` | 26 | Manual annotation results from Author 1 for the improved pilot sample. | Kết quả annotation thủ công của Author 1 cho tập pilot Improved. |
| `pilot_annotation_improved_author2.csv` | 26 | Manual annotation results from Author 2 for the improved pilot sample. | Kết quả annotation thủ công của Author 2 cho tập pilot Improved. |
| `pilot_ground_truth_improved.csv` | 26 | Final/reconciled ground truth for the improved pilot sample after comparing annotations. | Ground truth cuối cùng của tập pilot Improved sau khi đối chiếu annotation giữa các tác giả. |
| `kappa_scores_improved.csv` | 29 | Inter-annotator agreement file. It contains 26 issue-level score rows and 3 summary rows: `N`, `Cohen Kappa`, and `Agreement`. | File tính độ đồng thuận giữa annotator. File gồm 26 dòng điểm theo từng issue và 3 dòng tổng hợp: `N`, `Cohen Kappa`, `Agreement`. |

**Current pilot agreement / Độ đồng thuận pilot hiện tại:**

| Metric | Value |
| --- | ---: |
| `N` | 26 |
| `Cohen Kappa` | 0.7524 |
| `Agreement` | 22/26 |

---

## 5. Sample File Columns / Các cột trong file sample

The following columns appear in:

- `pilot_sample_improved.csv`
- `full_sample_improved.csv`

| Column | English Meaning | Ý nghĩa tiếng Việt |
| --- | --- | --- |
| `Issue Key` | Mojira issue identifier, for example `MC-299218`. | Mã issue trên Mojira, ví dụ `MC-299218`. |
| `Summary` | Short title or summary of the bug report. | Tiêu đề hoặc tóm tắt ngắn của bug report. |
| `Type` | Issue type, usually `Bug`. | Loại issue, thường là `Bug`. |
| `Affects Version/s` | Minecraft version(s) affected by the issue. | Phiên bản Minecraft bị ảnh hưởng bởi lỗi. |
| `Labels` | Labels/tags attached to the issue. | Nhãn/tag được gắn cho issue. |
| `Confirmation Status` | Confirmation state of the issue on Mojira. | Trạng thái xác nhận của issue trên Mojira. |
| `Category` | Category/component of the issue. | Nhóm hoặc thành phần liên quan đến issue. |
| `Resolution` | Final or current resolution status. | Trạng thái xử lý/kết luận của issue. |
| `Fix Version/s` | Version(s) where the issue is fixed, if available. | Phiên bản đã sửa lỗi, nếu có. |
| `Description` | Improved textual description of the bug. | Mô tả lỗi sau khi được cải thiện. |
| `Steps to Reproduce` | Improved steps for reproducing the bug. This is the key input for S2R evaluation. | Các bước tái hiện lỗi sau khi được cải thiện. Đây là phần quan trọng nhất để đánh giá S2R. |
| `Observed Behavior` | Actual behavior observed when the bug occurs. | Hành vi thực tế quan sát được khi lỗi xảy ra. |
| `Expected Behavior` | Expected/correct behavior of the system. | Hành vi mong đợi hoặc hành vi đúng của hệ thống. |
| `Environment` | Environment information such as Minecraft edition/version. | Thông tin môi trường như phiên bản hoặc edition của Minecraft. |

---

## 6. Annotation and Ground Truth Columns / Các cột annotation và ground truth

The following columns appear in:

- `pilot_annotation_improved_author1.csv`
- `pilot_annotation_improved_author2.csv`
- `pilot_ground_truth_improved.csv`
- `full_ground_truth_improved.csv`

| Column | English Meaning | Ý nghĩa tiếng Việt |
| --- | --- | --- |
| `BUG-ID` | Bug report identifier. In improved files, the value may include the suffix `Improved`. | Mã bug report. Trong file Improved, giá trị có thể có hậu tố `Improved`. |
| `S2R Label` | Label for Steps to Reproduce, such as `Executable` or `Non-Executable`. | Nhãn đánh giá phần Steps to Reproduce, ví dụ `Executable` hoặc `Non-Executable`. |
| `S2R Irrep Category` | Category explaining why the S2R is irreproducible/non-executable, if applicable. | Nhóm nguyên nhân khiến S2R không thể tái hiện/không thể thực thi, nếu có. |
| `Reason` | Explanation for the S2R label/category. | Lý do giải thích cho nhãn hoặc nhóm của S2R. |
| `OB Category` | Presence category for Observed Behavior. | Nhóm đánh giá sự hiện diện của Observed Behavior. |
| `OB Label` | Quality label for Observed Behavior, such as `Sufficient` or `Insufficient`. | Nhãn chất lượng của Observed Behavior, ví dụ `Sufficient` hoặc `Insufficient`. |
| `Reason.1` | Explanation for the OB label/category. | Lý do giải thích cho nhãn hoặc nhóm của Observed Behavior. |
| `EB Category` | Presence category for Expected Behavior. | Nhóm đánh giá sự hiện diện của Expected Behavior. |
| `EB Label` | Quality label for Expected Behavior, such as `Accurate` or another applicable label. | Nhãn chất lượng của Expected Behavior, ví dụ `Accurate` hoặc nhãn phù hợp khác. |
| `Reason.2` | Explanation for the EB label/category. | Lý do giải thích cho nhãn hoặc nhóm của Expected Behavior. |

**Note / Ghi chú:**  
If `pilot_ground_truth_improved.csv` contains empty columns such as `Unnamed: 10` or `Unnamed: 11`, they are likely export artifacts and should be ignored or removed before strict schema validation.

---

## 7. Kappa Score File / File kappa_scores_improved.csv

`kappa_scores_improved.csv` is used to summarize the agreement between two annotators during the pilot phase.

| Column | English Meaning | Ý nghĩa tiếng Việt |
| --- | --- | --- |
| `issue_key` | Issue key or summary row name. | Mã issue hoặc tên dòng tổng hợp. |
| `author1_score` | Numeric score assigned by Author 1. | Điểm số do Author 1 gán. |
| `author2_score` | Numeric score assigned by Author 2. | Điểm số do Author 2 gán. |
| `agree` | Agreement flag: `1` means both authors agree, `0` means disagreement. | Cờ đồng thuận: `1` nghĩa là hai tác giả đồng ý, `0` nghĩa là không đồng ý. |

The final rows summarize the pilot agreement:

N = 26  
Cohen Kappa = 0.7524  
Agreement = 22/26  

---

## 8. Recommended Workflow / Quy trình đề xuất

### 8.1 English Workflow

1. Use `pilot_sample_improved.csv` as the pilot input dataset.
2. Compare `pilot_annotation_improved_author1.csv` and `pilot_annotation_improved_author2.csv`.
3. Use `kappa_scores_improved.csv` to check inter-annotator agreement.
4. Create or verify `pilot_ground_truth_improved.csv`.
5. Run the LLM on `pilot_sample_improved.csv`.
6. Compare the LLM output with `pilot_ground_truth_improved.csv`.
7. After the pilot workflow is correct, run the LLM on `full_sample_improved.csv`.
8. Compare the full LLM output with `full_ground_truth_improved.csv`.
9. Compare Raw and Improved results to evaluate whether improved bug reports increase assessment quality.

### 8.2 Quy trình tiếng Việt

1. Dùng `pilot_sample_improved.csv` làm dữ liệu đầu vào cho giai đoạn pilot.
2. So sánh `pilot_annotation_improved_author1.csv` và `pilot_annotation_improved_author2.csv`.
3. Dùng `kappa_scores_improved.csv` để kiểm tra độ đồng thuận giữa hai annotator.
4. Tạo hoặc kiểm tra `pilot_ground_truth_improved.csv`.
5. Chạy LLM với `pilot_sample_improved.csv`.
6. So sánh kết quả LLM với `pilot_ground_truth_improved.csv`.
7. Khi quy trình pilot đã đúng, chạy LLM với `full_sample_improved.csv`.
8. So sánh kết quả LLM full với `full_ground_truth_improved.csv`.
9. So sánh kết quả Raw và Improved để đánh giá xem bug report đã cải thiện có giúp tăng chất lượng đánh giá hay không.

---

## 9. Data Usage Rules / Quy tắc sử dụng dữ liệu

### 9.1 English Data Usage Rules

- Keep the file names unchanged because scripts may depend on exact paths.
- Do not manually edit ground-truth files unless the team has agreed on the correction.
- Do not use ground-truth labels as input in LLM prompts.
- Store generated outputs in `Results/Improved`, not in `Data/Improved`.
- Treat `full_ground_truth_improved.csv` and `pilot_ground_truth_improved.csv` as reference labels.
- Treat `full_sample_improved.csv` and `pilot_sample_improved.csv` as LLM input data.
- The nested `IMPROVED/` folder should be kept as the original/extracted source folder unless the scripts explicitly require it.

### 9.2 Quy tắc sử dụng dữ liệu tiếng Việt

- Giữ nguyên tên file vì script có thể phụ thuộc vào đúng đường dẫn và đúng tên file.
- Không chỉnh sửa thủ công các file ground truth nếu nhóm chưa thống nhất.
- Không đưa nhãn ground truth vào prompt cho LLM.
- Lưu kết quả sinh ra vào `Results/Improved`, không lưu vào `Data/Improved`.
- Xem `full_ground_truth_improved.csv` và `pilot_ground_truth_improved.csv` là nhãn tham chiếu.
- Xem `full_sample_improved.csv` và `pilot_sample_improved.csv` là dữ liệu đầu vào cho LLM.
- Thư mục con `IMPROVED/` nên được giữ như thư mục nguồn/extracted ban đầu, trừ khi script yêu cầu dùng trực tiếp.

---

## 10. Relationship with Raw Dataset / Quan hệ với dữ liệu Raw

**English:**  
The Improved dataset should be evaluated in parallel with the Raw dataset. The Raw dataset represents the original bug reports, while the Improved dataset represents the refined bug reports. Comparing both versions helps determine whether improving bug report content makes LLM-based quality assessment more accurate or more consistent.

**Tiếng Việt:**  
Dữ liệu Improved nên được đánh giá song song với dữ liệu Raw. Dữ liệu Raw là bug report gốc, còn dữ liệu Improved là bug report đã được cải thiện. Việc so sánh hai phiên bản giúp xác định liệu việc cải thiện nội dung bug report có giúp LLM đánh giá chất lượng chính xác hoặc nhất quán hơn hay không.

---

## 11. Expected Result Files / Các file kết quả dự kiến

The following files should be generated outside this folder, under `Results/Improved`:

Results/Improved/  
├── pilot_llm_output_improved.csv  
├── pilot_api_log_improved.csv  
├── summary_improved.csv  
├── mismatch_analysis_improved.csv  
├── full_llm_output_improved.csv  
├── full_api_log_improved.csv  
├── summary_full_improved.csv  
└── mismatch_analysis_full_improved.csv  

**English:**  
These result files are not part of the source dataset. They are produced after running the LLM and evaluation scripts.

**Tiếng Việt:**  
Các file kết quả này không thuộc dữ liệu nguồn. Chúng được tạo ra sau khi chạy LLM và các script đánh giá.

---

## 12. Notes / Ghi chú

**English:**  
This README documents the data structure and meaning of files in `Data/Improved`. It should be updated whenever files are renamed, new columns are added, or the evaluation workflow changes.

**Tiếng Việt:**  
README này mô tả cấu trúc dữ liệu và ý nghĩa các file trong `Data/Improved`. Nên cập nhật file này khi đổi tên file, thêm cột mới hoặc thay đổi quy trình đánh giá.

---
