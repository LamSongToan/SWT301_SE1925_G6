# Raw Dataset README / Tài liệu bộ dữ liệu Raw

## 1. Overview / Tổng quan

English:

This folder stores the Raw version of the Mojira / Minecraft bug report
dataset. The Raw dataset contains the original bug reports before quality
improvement.

Tiếng Việt:

Thư mục này lưu phiên bản Raw của bộ dữ liệu bug report từ Mojira / Minecraft.
Bộ dữ liệu Raw chứa các bug report gốc trước khi được cải thiện chất lượng.

Main purpose:

    Use Raw bug reports as the baseline dataset for LLM-based reproducibility
    assessment.

Mục đích chính:

    Sử dụng bug report Raw làm bộ dữ liệu baseline cho việc đánh giá
    reproducibility bằng LLM.

## 2. Folder Contents / Nội dung thư mục

English:

Current files in this folder:

    full_ground_truth_raw.csv
    kappa_scores_raw.csv
    pilot_annotation_raw_author1.csv
    pilot_annotation_raw_author2.csv
    pilot_ground_truth_raw.csv
    pilot_sample_raw.csv
    README.md

Tiếng Việt:

Các file hiện tại trong thư mục này:

    full_ground_truth_raw.csv
    kappa_scores_raw.csv
    pilot_annotation_raw_author1.csv
    pilot_annotation_raw_author2.csv
    pilot_ground_truth_raw.csv
    pilot_sample_raw.csv
    README.md

## 3. File Descriptions / Mô tả các file

### 3.1 pilot_sample_raw.csv

English:

This file contains the Raw pilot sample used for initial LLM testing and
evaluation.

Tiếng Việt:

File này chứa tập mẫu Raw pilot dùng để chạy thử và đánh giá ban đầu với LLM.

Number of cases:

    26 cases

Số lượng case:

    26 case

### 3.2 pilot_ground_truth_raw.csv

English:

This file contains the final ground truth labels for the Raw pilot sample.

Tiếng Việt:

File này chứa nhãn ground truth cuối cùng cho tập Raw pilot.

Number of cases:

    26 cases

Số lượng case:

    26 case

Label distribution:

    Executable     : 10
    Non-Executable : 16

Phân bố nhãn:

    Executable     : 10
    Non-Executable : 16

### 3.3 full_ground_truth_raw.csv

English:

This file contains the full Raw ground truth dataset. It was generated from
Data/Annotations/Final Results.csv by selecting rows whose BUG-ID ends with Raw.

Tiếng Việt:

File này chứa toàn bộ ground truth của bộ dữ liệu Raw. File được tạo từ
Data/Annotations/Final Results.csv bằng cách chọn các dòng có BUG-ID kết thúc
bằng Raw.

Number of cases:

    139 cases

Số lượng case:

    139 case

Label distribution:

    Executable     : 40
    Non-Executable : 99

Phân bố nhãn:

    Executable     : 40
    Non-Executable : 99

### 3.4 pilot_annotation_raw_author1.csv

English:

This file contains Author 1's annotation labels for the Raw pilot sample.

Tiếng Việt:

File này chứa nhãn annotation của Author 1 cho tập Raw pilot.

Number of cases:

    26 cases

Số lượng case:

    26 case

Label distribution:

    Executable     : 10
    Non-Executable : 16

Phân bố nhãn:

    Executable     : 10
    Non-Executable : 16

### 3.5 pilot_annotation_raw_author2.csv

English:

This file contains Author 2's annotation labels for the Raw pilot sample.

Tiếng Việt:

File này chứa nhãn annotation của Author 2 cho tập Raw pilot.

Number of cases:

    26 cases

Số lượng case:

    26 case

Label distribution:

    Executable     : 9
    Non-Executable : 17

Phân bố nhãn:

    Executable     : 9
    Non-Executable : 17

### 3.6 kappa_scores_raw.csv

English:

This file stores the inter-annotator agreement result between Author 1 and
Author 2 for the Raw pilot sample.

Tiếng Việt:

File này lưu kết quả độ đồng thuận giữa Author 1 và Author 2 cho tập Raw pilot.

Agreement result:

    N             : 26
    Cohen Kappa   : 0.7647
    Agreement     : 22/26
    Threshold     : >= 0.70
    Status        : Passed

Kết quả đồng thuận:

    N             : 26
    Cohen Kappa   : 0.7647
    Agreement     : 22/26
    Threshold     : >= 0.70
    Status        : Passed

## 4. Validation Status / Trạng thái kiểm tra

English:

The Raw dataset has passed the validation check. All required files exist, and
the pilot issue keys are consistent across sample, ground truth, annotation,
and kappa files.

Tiếng Việt:

Bộ dữ liệu Raw đã vượt qua bước kiểm tra. Tất cả các file cần thiết đều tồn tại,
và các issue key của tập pilot khớp giữa sample, ground truth, annotation, và
file kappa.

Validation command:

    .\.venv\Scripts\python.exe Scripts\Raw\check_raw_data.py

Lệnh kiểm tra:

    .\.venv\Scripts\python.exe Scripts\Raw\check_raw_data.py

Validation result:

    Raw data check: PASSED

Kết quả kiểm tra:

    Raw data check: PASSED

## 5. Usage / Cách sử dụng

English:

Use this dataset when running LLM experiments on the original bug reports.

Tiếng Việt:

Sử dụng bộ dữ liệu này khi chạy thí nghiệm LLM trên các bug report gốc.

Expected future input files:

    pilot_sample_raw.csv
    pilot_ground_truth_raw.csv
    full_ground_truth_raw.csv

Các file đầu vào dự kiến:

    pilot_sample_raw.csv
    pilot_ground_truth_raw.csv
    full_ground_truth_raw.csv

Expected future output folder:

    Results/Raw/

Thư mục output dự kiến:

    Results/Raw/

## 6. Important Notes / Ghi chú quan trọng

English:

Do not manually modify labels in this folder unless there is a documented
correction. LLM result files should not be stored in Data/Raw. They should be
stored in Results/Raw.

Tiếng Việt:

Không tự ý chỉnh sửa nhãn trong thư mục này nếu không có ghi chú chỉnh sửa rõ
ràng. Các file kết quả của LLM không nên lưu trong Data/Raw mà nên lưu trong
Results/Raw.
