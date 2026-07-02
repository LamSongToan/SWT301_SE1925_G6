# Improved Dataset README / Tài liệu bộ dữ liệu Improved

## 1. Overview / Tổng quan

English:

This folder stores the Improved version of the Mojira / Minecraft bug report
dataset. The Improved dataset contains bug reports after quality improvement,
especially in Steps to Reproduce, Observed Behavior, and Expected Behavior.

Tiếng Việt:

Thư mục này lưu phiên bản Improved của bộ dữ liệu bug report từ Mojira /
Minecraft. Bộ dữ liệu Improved chứa các bug report sau khi được cải thiện chất
lượng, đặc biệt ở phần Steps to Reproduce, Observed Behavior, và Expected
Behavior.

Main purpose:

    Use Improved bug reports to evaluate whether better bug report quality helps
    the LLM produce reproducibility assessments that are closer to human ground
    truth.

Mục đích chính:

    Sử dụng bug report Improved để đánh giá xem việc cải thiện chất lượng bug
    report có giúp LLM đưa ra đánh giá reproducibility gần với human ground truth
    hơn hay không.

## 2. Folder Contents / Nội dung thư mục

English:

Current files in this folder:

    full_ground_truth_improved.csv
    kappa_scores_improved.csv
    pilot_annotation_improved_author1.csv
    pilot_annotation_improved_author2.csv
    pilot_ground_truth_improved.csv
    pilot_sample_improved.csv
    README.md

Tiếng Việt:

Các file hiện tại trong thư mục này:

    full_ground_truth_improved.csv
    kappa_scores_improved.csv
    pilot_annotation_improved_author1.csv
    pilot_annotation_improved_author2.csv
    pilot_ground_truth_improved.csv
    pilot_sample_improved.csv
    README.md

## 3. File Descriptions / Mô tả các file

### 3.1 pilot_sample_improved.csv

English:

This file contains the Improved pilot sample used for initial LLM testing and
evaluation.

Tiếng Việt:

File này chứa tập mẫu Improved pilot dùng để chạy thử và đánh giá ban đầu với
LLM.

Number of cases:

    26 cases

Số lượng case:

    26 case

### 3.2 pilot_ground_truth_improved.csv

English:

This file contains the final ground truth labels for the Improved pilot sample.

Tiếng Việt:

File này chứa nhãn ground truth cuối cùng cho tập Improved pilot.

Number of cases:

    26 cases

Số lượng case:

    26 case

Label distribution:

    Executable     : 19
    Non-Executable : 7

Phân bố nhãn:

    Executable     : 19
    Non-Executable : 7

### 3.3 full_ground_truth_improved.csv

English:

This file contains the full Improved ground truth dataset. It was generated from
Data/Annotations/Final Results.csv by selecting rows whose BUG-ID ends with
Improved.

Tiếng Việt:

File này chứa toàn bộ ground truth của bộ dữ liệu Improved. File được tạo từ
Data/Annotations/Final Results.csv bằng cách chọn các dòng có BUG-ID kết thúc
bằng Improved.

Number of cases:

    139 cases

Số lượng case:

    139 case

Label distribution:

    Executable     : 94
    Non-Executable : 45

Phân bố nhãn:

    Executable     : 94
    Non-Executable : 45

### 3.4 pilot_annotation_improved_author1.csv

English:

This file contains Author 1's annotation labels for the Improved pilot sample.

Tiếng Việt:

File này chứa nhãn annotation của Author 1 cho tập Improved pilot.

Number of cases:

    26 cases

Số lượng case:

    26 case

Label distribution:

    Executable     : 19
    Non-Executable : 7

Phân bố nhãn:

    Executable     : 19
    Non-Executable : 7

### 3.5 pilot_annotation_improved_author2.csv

English:

This file contains Author 2's annotation labels for the Improved pilot sample.

Tiếng Việt:

File này chứa nhãn annotation của Author 2 cho tập Improved pilot.

Number of cases:

    26 cases

Số lượng case:

    26 case

Label distribution:

    Executable     : 18
    Non-Executable : 8

Phân bố nhãn:

    Executable     : 18
    Non-Executable : 8

### 3.6 kappa_scores_improved.csv

English:

This file stores the inter-annotator agreement result between Author 1 and
Author 2 for the Improved pilot sample.

Tiếng Việt:

File này lưu kết quả độ đồng thuận giữa Author 1 và Author 2 cho tập Improved
pilot.

Agreement result:

    N             : 26
    Cohen Kappa   : 0.7524
    Agreement     : 22/26
    Threshold     : >= 0.70
    Status        : Passed

Kết quả đồng thuận:

    N             : 26
    Cohen Kappa   : 0.7524
    Agreement     : 22/26
    Threshold     : >= 0.70
    Status        : Passed

## 4. Validation Status / Trạng thái kiểm tra

English:

The Improved dataset has passed the validation check. All required files exist,
and the pilot issue keys are consistent across sample, ground truth,
annotation, and kappa files.

Tiếng Việt:

Bộ dữ liệu Improved đã vượt qua bước kiểm tra. Tất cả các file cần thiết đều tồn
tại, và các issue key của tập pilot khớp giữa sample, ground truth, annotation,
và file kappa.

Validation command:

    .\.venv\Scripts\python.exe Scripts\Improved\check_improved_data.py

Lệnh kiểm tra:

    .\.venv\Scripts\python.exe Scripts\Improved\check_improved_data.py

Validation result:

    Improved data check: PASSED

Kết quả kiểm tra:

    Improved data check: PASSED

## 5. Usage / Cách sử dụng

English:

Use this dataset when running LLM experiments on improved bug reports.

Tiếng Việt:

Sử dụng bộ dữ liệu này khi chạy thí nghiệm LLM trên các bug report đã được cải
thiện.

Expected future input files:

    pilot_sample_improved.csv
    pilot_ground_truth_improved.csv
    full_ground_truth_improved.csv

Các file đầu vào dự kiến:

    pilot_sample_improved.csv
    pilot_ground_truth_improved.csv
    full_ground_truth_improved.csv

Expected future output folder:

    Results/Improved/

Thư mục output dự kiến:

    Results/Improved/

## 6. Important Notes / Ghi chú quan trọng

English:

Do not manually modify labels in this folder unless there is a documented
correction. LLM result files should not be stored in Data/Improved. They should
be stored in Results/Improved.

Tiếng Việt:

Không tự ý chỉnh sửa nhãn trong thư mục này nếu không có ghi chú chỉnh sửa rõ
ràng. Các file kết quả của LLM không nên lưu trong Data/Improved mà nên lưu
trong Results/Improved.
