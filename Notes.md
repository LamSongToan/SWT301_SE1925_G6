# Project Notes / Ghi chú dự án

## 1. Current Project Status / Trạng thái hiện tại của dự án

English:

This project has completed the data preparation structure for both Raw and Improved datasets. The current work focuses on organizing the dataset into two parallel versions so that later experiments can compare LLM performance on the original bug reports and the improved bug reports.

Tiếng Việt:

Dự án đã hoàn thành bước chuẩn bị cấu trúc dữ liệu cho cả hai bộ dữ liệu Raw và Improved. Công việc hiện tại tập trung vào việc tổ chức dữ liệu thành hai phiên bản song song để các thí nghiệm sau này có thể so sánh hiệu quả của LLM trên bug report gốc và bug report đã được cải thiện.

Main comparison / So sánh chính:

    Raw bug reports vs Improved bug reports
    Bug report Raw so với bug report Improved

Purpose / Mục đích:

    Evaluate whether improving bug report quality can improve reproducibility assessment and agreement between LLM prediction and human ground truth.
    Đánh giá xem việc cải thiện chất lượng bug report có giúp cải thiện khả năng đánh giá reproducibility và mức độ đồng thuận giữa dự đoán của LLM với ground truth do con người xác định hay không.

## 2. Research Context / Bối cảnh nghiên cứu

English:

The research topic focuses on automatic bug report quality assessment using large language models. The main quality criterion in the current project is reproducibility, especially whether the Steps to Reproduce are executable.

Tiếng Việt:

Chủ đề nghiên cứu tập trung vào việc đánh giá chất lượng bug report tự động bằng mô hình ngôn ngữ lớn. Tiêu chí chất lượng chính trong dự án hiện tại là reproducibility, đặc biệt là việc Steps to Reproduce có thể thực hiện được hay không.

Research question / Câu hỏi nghiên cứu:

    For bug reports on Mojira / Minecraft Issue Tracker, can an LLM automatically assess bug report quality based on reproducibility criteria, compared with human manual review, and achieve Cohen's Kappa >= 0.70?
    Đối với các báo cáo lỗi trên Mojira / Minecraft Issue Tracker, LLM có thể tự động đánh giá chất lượng bug report theo tiêu chí reproducibility, so với đánh giá thủ công của con người, và đạt Cohen's Kappa >= 0.70 hay không?

Main metric / Chỉ số đánh giá chính:

    Cohen's Kappa

Research threshold / Ngưỡng nghiên cứu:

    Cohen's Kappa >= 0.70

## 3. Dataset Source / Nguồn dữ liệu

English:

The dataset is based on the ImproBR Replication Package. The dataset domain is Mojira / Minecraft Issue Tracker bug reports.

Tiếng Việt:

Bộ dữ liệu được lấy dựa trên ImproBR Replication Package. Miền dữ liệu là các bug report từ Mojira / Minecraft Issue Tracker.

Original source / Nguồn gốc:

    ImproBR Replication Package

Platform / Nền tảng:

    Figshare

Dataset domain / Miền dữ liệu:

    Mojira / Minecraft Issue Tracker bug reports
    Bug report từ Mojira / Minecraft Issue Tracker

Source page / Trang nguồn:

    https://figshare.com/articles/software/ImproBR_Replication_Package/30086083

License note / Ghi chú về giấy phép:

    The dataset license should be verified from the original Figshare package or the original README file.
    Giấy phép của bộ dữ liệu cần được kiểm tra lại từ package gốc trên Figshare hoặc từ README gốc của package.

## 4. Data Folder Structure / Cấu trúc thư mục Data

English:

The Data folder is organized into three main parts: Annotations, Raw, and Improved.

Tiếng Việt:

Thư mục Data được tổ chức thành ba phần chính: Annotations, Raw, và Improved.

Current structure / Cấu trúc hiện tại:

    Data/
    ├── Annotations/
    ├── Raw/
    └── Improved/

## 5. Data/Annotations

English:

This folder stores the original annotation source files. These files are the main annotation sources used to derive ground truth files for both Raw and Improved datasets.

Tiếng Việt:

Thư mục này lưu các file annotation gốc. Các file này là nguồn annotation chính được dùng để tạo ra ground truth cho cả hai bộ dữ liệu Raw và Improved.

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

## 6. Data/Raw

English:

This folder stores the Raw version of the dataset. The Raw dataset represents the original bug reports before quality improvement. It is used as the baseline for comparison with the Improved dataset.

Tiếng Việt:

Thư mục này lưu phiên bản Raw của bộ dữ liệu. Dữ liệu Raw là các bug report gốc trước khi được cải thiện chất lượng. Bộ dữ liệu này được dùng làm baseline để so sánh với bộ dữ liệu Improved.

Current files / Các file hiện tại:

    Data/Raw/
    ├── full_ground_truth_raw.csv
    ├── kappa_scores_raw.csv
    ├── pilot_annotation_raw_author1.csv
    ├── pilot_annotation_raw_author2.csv
    ├── pilot_ground_truth_raw.csv
    ├── pilot_sample_raw.csv
    └── README.md

## 7. Data/Improved

English:

This folder stores the Improved version of the dataset. The Improved dataset represents bug reports after quality improvement, especially for Steps to Reproduce, Observed Behavior, and Expected Behavior.

Tiếng Việt:

Thư mục này lưu phiên bản Improved của bộ dữ liệu. Dữ liệu Improved là các bug report sau khi đã được cải thiện chất lượng, đặc biệt ở phần Steps to Reproduce, Observed Behavior, và Expected Behavior.

Current files / Các file hiện tại:

    Data/Improved/
    ├── full_ground_truth_improved.csv
    ├── kappa_scores_improved.csv
    ├── pilot_annotation_improved_author1.csv
    ├── pilot_annotation_improved_author2.csv
    ├── pilot_ground_truth_improved.csv
    ├── pilot_sample_improved.csv
    └── README.md

## 8. Raw Dataset Validation Result / Kết quả kiểm tra dữ liệu Raw

English:

The Raw dataset was validated using the Raw checking script. All required data files were found, and all pilot issue keys are consistent across sample, annotation, ground truth, and kappa files.

Tiếng Việt:

Bộ dữ liệu Raw đã được kiểm tra bằng script kiểm tra Raw. Tất cả các file dữ liệu cần thiết đều được tìm thấy, và các issue key của tập pilot đều khớp giữa sample, annotation, ground truth, và file kappa.

Validation command / Lệnh kiểm tra:

    .\.venv\Scripts\python.exe Scripts\Raw\check_raw_data.py

Required files status / Trạng thái các file bắt buộc:

    FOUND: full_ground_truth_raw.csv
    FOUND: kappa_scores_raw.csv
    FOUND: pilot_annotation_raw_author1.csv
    FOUND: pilot_annotation_raw_author2.csv
    FOUND: pilot_ground_truth_raw.csv
    FOUND: pilot_sample_raw.csv

Row count / Số lượng dòng dữ liệu:

    pilot_sample_raw.csv              : 26 cases
    pilot_ground_truth_raw.csv        : 26 cases
    full_ground_truth_raw.csv         : 139 cases
    pilot_annotation_raw_author1.csv  : 26 cases
    pilot_annotation_raw_author2.csv  : 26 cases
    kappa_scores_raw.csv              : 26 case rows

Pilot issue key consistency / Độ khớp issue key của tập pilot:

    pilot_sample_raw.csv vs pilot_ground_truth_raw.csv       : OK
    pilot_sample_raw.csv vs pilot_annotation_raw_author1.csv : OK
    pilot_sample_raw.csv vs pilot_annotation_raw_author2.csv : OK
    pilot_sample_raw.csv vs kappa_scores_raw.csv             : OK

S2R label distribution / Phân bố nhãn S2R:

    Pilot Ground Truth:
    Executable     : 10
    Non-Executable : 16

    Full Ground Truth:
    Executable     : 40
    Non-Executable : 99

    Author 1:
    Executable     : 10
    Non-Executable : 16

    Author 2:
    Executable     : 9
    Non-Executable : 17

Raw pilot inter-annotator agreement / Độ đồng thuận giữa hai người chấm cho Raw pilot:

    N             : 26
    Cohen Kappa   : 0.7647
    Agreement     : 22/26
    Threshold     : >= 0.70
    Status        : Passed

Conclusion / Kết luận:

    Data/Raw is valid and ready for Raw-side LLM experiments.
    Data/Raw hợp lệ và đã sẵn sàng cho thí nghiệm LLM phía Raw.

## 9. Improved Dataset Validation Result / Kết quả kiểm tra dữ liệu Improved

English:

The Improved dataset was validated using the Improved checking script. All required data files were found, and all pilot issue keys are consistent across sample, annotation, ground truth, and kappa files.

Tiếng Việt:

Bộ dữ liệu Improved đã được kiểm tra bằng script kiểm tra Improved. Tất cả các file dữ liệu cần thiết đều được tìm thấy, và các issue key của tập pilot đều khớp giữa sample, annotation, ground truth, và file kappa.

Validation command / Lệnh kiểm tra:

    .\.venv\Scripts\python.exe Scripts\Improved\check_improved_data.py

Required files status / Trạng thái các file bắt buộc:

    FOUND: full_ground_truth_improved.csv
    FOUND: kappa_scores_improved.csv
    FOUND: pilot_annotation_improved_author1.csv
    FOUND: pilot_annotation_improved_author2.csv
    FOUND: pilot_ground_truth_improved.csv
    FOUND: pilot_sample_improved.csv

Row count / Số lượng dòng dữ liệu:

    pilot_sample_improved.csv              : 26 cases
    pilot_ground_truth_improved.csv        : 26 cases
    full_ground_truth_improved.csv         : 139 cases
    pilot_annotation_improved_author1.csv  : 26 cases
    pilot_annotation_improved_author2.csv  : 26 cases
    kappa_scores_improved.csv              : 26 case rows

Pilot issue key consistency / Độ khớp issue key của tập pilot:

    pilot_sample_improved.csv vs pilot_ground_truth_improved.csv       : OK
    pilot_sample_improved.csv vs pilot_annotation_improved_author1.csv : OK
    pilot_sample_improved.csv vs pilot_annotation_improved_author2.csv : OK
    pilot_sample_improved.csv vs kappa_scores_improved.csv             : OK

S2R label distribution / Phân bố nhãn S2R:

    Pilot Ground Truth:
    Executable     : 19
    Non-Executable : 7

    Full Ground Truth:
    Executable     : 94
    Non-Executable : 45

    Author 1:
    Executable     : 19
    Non-Executable : 7

    Author 2:
    Executable     : 18
    Non-Executable : 8

Improved pilot inter-annotator agreement / Độ đồng thuận giữa hai người chấm cho Improved pilot:

    N             : 26
    Cohen Kappa   : 0.7524
    Agreement     : 22/26
    Threshold     : >= 0.70
    Status        : Passed

Conclusion / Kết luận:

    Data/Improved is valid and ready for Improved-side LLM experiments.
    Data/Improved hợp lệ và đã sẵn sàng cho thí nghiệm LLM phía Improved.

## 10. Ground Truth Generation / Cách tạo Ground Truth

English:

The full ground truth files for Raw and Improved were generated from the same source file, Data/Annotations/Final Results.csv. The Raw file selects rows whose BUG-ID ends with Raw, while the Improved file selects rows whose BUG-ID ends with Improved.

Tiếng Việt:

Các file full ground truth cho Raw và Improved được tạo từ cùng một file nguồn, Data/Annotations/Final Results.csv. File Raw lấy các dòng có BUG-ID kết thúc bằng Raw, còn file Improved lấy các dòng có BUG-ID kết thúc bằng Improved.

### 10.1 Raw Full Ground Truth / Full Ground Truth của Raw

Generated file / File được tạo:

    Data/Raw/full_ground_truth_raw.csv

Source file / File nguồn:

    Data/Annotations/Final Results.csv

Generation rule / Quy tắc tạo file:

    Only rows whose BUG-ID ends with Raw are selected.
    Chỉ lấy các dòng có BUG-ID kết thúc bằng Raw.

Command / Lệnh chạy:

    .\.venv\Scripts\python.exe Scripts\Raw\create_full_ground_truth_raw.py

Expected result / Kết quả mong đợi:

    Raw cases: 139

### 10.2 Improved Full Ground Truth / Full Ground Truth của Improved

Generated file / File được tạo:

    Data/Improved/full_ground_truth_improved.csv

Source file / File nguồn:

    Data/Annotations/Final Results.csv

Generation rule / Quy tắc tạo file:

    Only rows whose BUG-ID ends with Improved are selected.
    Chỉ lấy các dòng có BUG-ID kết thúc bằng Improved.

Command / Lệnh chạy:

    .\.venv\Scripts\python.exe Scripts\Improved\create_full_ground_truth_improved.py

Expected result / Kết quả mong đợi:

    Improved cases: 139

## 11. Results Folder Structure / Cấu trúc thư mục Results

English:

The Results folder is prepared for future LLM outputs. At this stage, only README.md and .gitkeep files are kept in each result subfolder. Empty CSV or TXT output files should not be created manually.

Tiếng Việt:

Thư mục Results được chuẩn bị để chứa output của LLM trong tương lai. Ở giai đoạn này, mỗi thư mục kết quả chỉ giữ README.md và .gitkeep. Không nên tự tạo các file CSV hoặc TXT rỗng.

Current structure / Cấu trúc hiện tại:

    Results/
    ├── Raw/
    │   ├── README.md
    │   └── .gitkeep
    └── Improved/
        ├── README.md
        └── .gitkeep

Important rule / Quy tắc quan trọng:

    Do not create empty CSV or TXT result files manually.
    Không tự tạo các file kết quả CSV hoặc TXT rỗng.

Reason / Lý do:

    Empty result files may be mistaken for completed experiment outputs. All result files should be generated by experiment scripts.
    Các file kết quả rỗng có thể bị hiểu nhầm là output thí nghiệm đã hoàn thành. Tất cả file kết quả nên được sinh ra bởi script thí nghiệm.

## 12. Raw Results Status / Trạng thái Results của Raw

English:

The Raw results folder is prepared, but LLM output files are still pending.

Tiếng Việt:

Thư mục kết quả Raw đã được chuẩn bị, nhưng các file output của LLM vẫn đang ở trạng thái pending.

Validation result / Kết quả kiểm tra:

    Results/Raw/README.md : FOUND
    Results/Raw/.gitkeep  : FOUND

Pending output files / Các file output đang pending:

    pilot_llm_output_raw.csv
    pilot_api_log_raw.txt
    full_llm_output_raw.csv
    full_api_log_raw.txt
    summary_raw.csv
    mismatch_analysis_raw.csv

Status / Trạng thái:

    Results/Raw is ready, but Raw LLM output files are still pending.
    Results/Raw đã sẵn sàng, nhưng các file output LLM của Raw vẫn đang pending.

## 13. Improved Results Status / Trạng thái Results của Improved

English:

The Improved results folder is prepared, but LLM output files are still pending.

Tiếng Việt:

Thư mục kết quả Improved đã được chuẩn bị, nhưng các file output của LLM vẫn đang ở trạng thái pending.

Validation result / Kết quả kiểm tra:

    Results/Improved/README.md : FOUND
    Results/Improved/.gitkeep  : FOUND

Pending output files / Các file output đang pending:

    pilot_llm_output_improved.csv
    pilot_api_log_improved.txt
    full_llm_output_improved.csv
    full_api_log_improved.txt
    summary_improved.csv
    mismatch_analysis_improved.csv

Status / Trạng thái:

    Results/Improved is ready, but Improved LLM output files are still pending.
    Results/Improved đã sẵn sàng, nhưng các file output LLM của Improved vẫn đang pending.

## 14. Scripts Added or Updated / Các script đã thêm hoặc cập nhật

English:

Helper scripts were added or updated for checking Raw and Improved data folders and generating full ground truth files.

Tiếng Việt:

Các script hỗ trợ đã được thêm hoặc cập nhật để kiểm tra thư mục dữ liệu Raw và Improved, đồng thời tạo các file full ground truth.

### 14.1 Raw Scripts / Script cho Raw

Current Raw helper scripts / Các script hỗ trợ Raw hiện tại:

    Scripts/Raw/
    ├── check_raw_data.py
    └── create_full_ground_truth_raw.py

Purpose / Mục đích:

    check_raw_data.py validates Data/Raw and checks Results/Raw status.
    check_raw_data.py kiểm tra Data/Raw và trạng thái Results/Raw.

    create_full_ground_truth_raw.py generates full_ground_truth_raw.csv from Data/Annotations/Final Results.csv.
    create_full_ground_truth_raw.py tạo full_ground_truth_raw.csv từ Data/Annotations/Final Results.csv.

### 14.2 Improved Scripts / Script cho Improved

Current Improved helper scripts / Các script hỗ trợ Improved hiện tại:

    Scripts/Improved/
    ├── check_improved_data.py
    └── create_full_ground_truth_improved.py

Purpose / Mục đích:

    check_improved_data.py validates Data/Improved and checks Results/Improved status.
    check_improved_data.py kiểm tra Data/Improved và trạng thái Results/Improved.

    create_full_ground_truth_improved.py generates full_ground_truth_improved.csv from Data/Annotations/Final Results.csv.
    create_full_ground_truth_improved.py tạo full_ground_truth_improved.csv từ Data/Annotations/Final Results.csv.

Path rule / Quy tắc đường dẫn:

    Scripts inside Scripts/Raw/ or Scripts/Improved/ should use:
    Các script nằm trong Scripts/Raw/ hoặc Scripts/Improved/ nên dùng:

    BASE_DIR = Path(__file__).resolve().parents[2]

Reason / Lý do:

    parents[2] points back to the project root folder SWT301_SE1925_G6.
    parents[2] trỏ ngược về thư mục gốc của project SWT301_SE1925_G6.

## 15. Current Overall Status / Trạng thái tổng thể hiện tại

English:

The data preparation work for both Raw and Improved datasets has been completed. Both datasets passed validation checks. The Results folders are prepared but do not yet contain real LLM output files.

Tiếng Việt:

Phần chuẩn bị dữ liệu cho cả hai bộ Raw và Improved đã hoàn tất. Cả hai bộ dữ liệu đều đã vượt qua bước kiểm tra. Các thư mục Results đã được chuẩn bị nhưng chưa có file output thật từ LLM.

Data preparation status / Trạng thái chuẩn bị dữ liệu:

    Data/Annotations  : DONE
    Data/Raw          : DONE
    Data/Improved     : DONE
    Results/Raw       : READY - pending LLM output
    Results/Improved  : READY - pending LLM output

Validation status / Trạng thái kiểm tra:

    Raw data check      : PASSED
    Improved data check : PASSED

Role status / Trạng thái vai trò:

    LR / data preparation work is completed for the Raw and Improved dataset structure.
    Phần việc LR / chuẩn bị dữ liệu đã hoàn thành cho cấu trúc dữ liệu Raw và Improved.

## 16. Next Step / Bước tiếp theo

English:

The next stage is to update experiment and metric scripts so that LLM experiments can run separately on Raw and Improved datasets.

Tiếng Việt:

Giai đoạn tiếp theo là cập nhật các script chạy thí nghiệm và script tính metric để LLM có thể chạy riêng trên bộ dữ liệu Raw và Improved.

Target commands for future implementation / Các lệnh mục tiêu cho phần triển khai sau này:

    .\.venv\Scripts\python.exe Scripts\run_experiment.py --version raw --phase pilot
    .\.venv\Scripts\python.exe Scripts\run_experiment.py --version improved --phase pilot
    .\.venv\Scripts\python.exe Scripts\run_experiment.py --version raw --phase full
    .\.venv\Scripts\python.exe Scripts\run_experiment.py --version improved --phase full

Expected future output files for Raw / Các file output dự kiến cho Raw:

    Results/Raw/pilot_llm_output_raw.csv
    Results/Raw/pilot_api_log_raw.txt
    Results/Raw/full_llm_output_raw.csv
    Results/Raw/full_api_log_raw.txt
    Results/Raw/summary_raw.csv
    Results/Raw/mismatch_analysis_raw.csv

Expected future output files for Improved / Các file output dự kiến cho Improved:

    Results/Improved/pilot_llm_output_improved.csv
    Results/Improved/pilot_api_log_improved.txt
    Results/Improved/full_llm_output_improved.csv
    Results/Improved/full_api_log_improved.txt
    Results/Improved/summary_improved.csv
    Results/Improved/mismatch_analysis_improved.csv

## 17. Raw vs Improved Comparison Plan / Kế hoạch so sánh Raw và Improved

English:

After LLM output and metric files are generated, Raw and Improved results should be compared using their summary files. The final comparison will show whether the Improved bug reports help the LLM produce predictions closer to human ground truth.

Tiếng Việt:

Sau khi output của LLM và các file metric được tạo, kết quả Raw và Improved sẽ được so sánh bằng các file summary. Kết quả so sánh cuối cùng sẽ cho thấy liệu bug report Improved có giúp LLM đưa ra dự đoán gần với human ground truth hơn so với bug report Raw hay không.

Comparison input files / Các file đầu vào để so sánh:

    Results/Raw/summary_raw.csv
    Results/Improved/summary_improved.csv

Main comparison metrics / Các metric so sánh chính:

    Accuracy
    Cohen's Kappa
    Correct predictions
    Incorrect predictions
    Threshold passed
    Total cost USD

    Accuracy
    Cohen's Kappa
    Số dự đoán đúng
    Số dự đoán sai
    Trạng thái đạt ngưỡng
    Tổng chi phí USD

Expected final comparison file / File so sánh cuối cùng dự kiến:

    Results/comparison_raw_vs_improved.csv

Purpose / Mục đích:

    This comparison will show whether the Improved bug reports help the LLM produce predictions that are closer to the human ground truth compared with the Raw bug reports.
    Phần so sánh này sẽ cho biết liệu bug report Improved có giúp LLM đưa ra dự đoán gần với human ground truth hơn so với bug report Raw hay không.
